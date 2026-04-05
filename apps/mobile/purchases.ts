import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import { Platform } from "react-native";
import Purchases, {
  LOG_LEVEL,
  PRODUCT_CATEGORY,
  type CustomerInfo,
  type PurchasesStoreProduct,
} from "react-native-purchases";

const ADS_REMOVED_STORAGE_KEY = "trace.adsRemoved";
const REVENUECAT_IOS_API_KEY =
  process.env.EXPO_PUBLIC_REVENUECAT_IOS_API_KEY ?? "";
const REVENUECAT_IOS_API_KEY_ENV_NAME = "EXPO_PUBLIC_REVENUECAT_IOS_API_KEY";

export const REMOVE_ADS_PRODUCT_ID = "com.trace.removeads";
export const REMOVE_ADS_PRICE_LABEL = "$3.99";

type PurchaseResult = {
  restored: boolean;
};

function hasRemoveAdsAccess(customerInfo: CustomerInfo) {
  return customerInfo.allPurchasedProductIdentifiers.includes(
    REMOVE_ADS_PRODUCT_ID,
  );
}

async function persistAdsRemoved(value: boolean) {
  await AsyncStorage.setItem(ADS_REMOVED_STORAGE_KEY, String(value));
}

async function configurePurchasesIfNeeded() {
  if (Platform.OS !== "ios" || !REVENUECAT_IOS_API_KEY) {
    return false;
  }

  if (!Purchases.isConfigured()) {
    Purchases.setLogLevel(LOG_LEVEL.WARN);
    Purchases.configure({ apiKey: REVENUECAT_IOS_API_KEY });
  }

  return true;
}

async function getRemoveAdsProduct() {
  const products = await Purchases.getProducts(
    [REMOVE_ADS_PRODUCT_ID],
    PRODUCT_CATEGORY.NON_SUBSCRIPTION,
  );

  return products[0] ?? null;
}

function getReadablePurchaseError(error: unknown) {
  if (
    typeof error === "object" &&
    error !== null &&
    "userCancelled" in error &&
    error.userCancelled
  ) {
    return "Purchase cancelled.";
  }

  if (
    typeof error === "object" &&
    error !== null &&
    "message" in error &&
    typeof error.message === "string" &&
    error.message
  ) {
    return error.message;
  }

  return "Unable to complete the purchase right now.";
}

export function usePurchaseState() {
  const [adsRemoved, setAdsRemoved] = useState(false);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    async function loadPurchaseState() {
      let persistedAdsRemoved = false;

      try {
        const savedValue = await AsyncStorage.getItem(ADS_REMOVED_STORAGE_KEY);
        persistedAdsRemoved = savedValue === "true";
        setAdsRemoved(persistedAdsRemoved);
      } catch {
        setAdsRemoved(false);
      }

      try {
        const purchasesConfigured = await configurePurchasesIfNeeded();
        if (purchasesConfigured) {
          const customerInfo = await Purchases.getCustomerInfo();
          if (hasRemoveAdsAccess(customerInfo)) {
            await persistAdsRemoved(true);
            setAdsRemoved(true);
          } else if (!persistedAdsRemoved) {
            setAdsRemoved(false);
          }
        }
      } catch {
        setAdsRemoved(persistedAdsRemoved);
      } finally {
        setIsReady(true);
      }
    }

    void loadPurchaseState();
  }, []);

  async function removeAds() {
    const purchasesConfigured = await configurePurchasesIfNeeded();
    if (!purchasesConfigured) {
      throw new Error(
        `Purchases are not configured for this iOS build yet. Set ${REVENUECAT_IOS_API_KEY_ENV_NAME} and use a development build.`,
      );
    }

    try {
      const product = await getRemoveAdsProduct();
      if (!product) {
        throw new Error("Remove Ads is not available right now.");
      }

      const purchaseResult = await Purchases.purchaseStoreProduct(
        product as PurchasesStoreProduct,
      );

      if (hasRemoveAdsAccess(purchaseResult.customerInfo)) {
        await persistAdsRemoved(true);
        setAdsRemoved(true);
        return;
      }

      throw new Error("Purchase completed, but Remove Ads was not unlocked.");
    } catch (error) {
      throw new Error(getReadablePurchaseError(error));
    }
  }

  async function restorePurchases(): Promise<PurchaseResult> {
    const purchasesConfigured = await configurePurchasesIfNeeded();
    if (!purchasesConfigured) {
      throw new Error(
        `Purchases are not configured for this iOS build yet. Set ${REVENUECAT_IOS_API_KEY_ENV_NAME} and use a development build.`,
      );
    }

    try {
      const customerInfo = await Purchases.restorePurchases();
      const restored = hasRemoveAdsAccess(customerInfo);

      if (restored) {
        await persistAdsRemoved(true);
        setAdsRemoved(true);
      }

      return { restored };
    } catch (error) {
      throw new Error(getReadablePurchaseError(error));
    }
  }

  return {
    adsRemoved,
    isReady,
    removeAds,
    restorePurchases,
  };
}
