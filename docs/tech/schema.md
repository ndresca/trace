# Trace Schemas

## Entity Schema

An entity represents one famous person that the app may guess.

### Required Fields

- `id`  
  Stable unique identifier for the person.

- `name`  
  Display name of the person.

- `aliases`  
  Optional alternate names or common spellings.

- `short_description`  
  Brief human-readable summary.

- `attributes`  
  Key-value map used by the engine. Each key should match a question `attribute_key`.

## Example Entity

```json
{
  "id": "taylor_swift",
  "name": "Taylor Swift",
  "aliases": ["Taylor Alison Swift"],
  "short_description": "American singer-songwriter",
  "attributes": {
    "is_musician": true,
    "is_actor": false,
    "is_female": true,
    "is_alive": true,
    "primarily_known_for_music": true
  }
}
```

## Question Schema

A question represents one askable prompt in the game.

### Required Fields

- `id`  
  Stable unique identifier for the question.

- `text`  
  User-facing question text.

- `attribute_key`  
  Attribute that the question is intended to measure.

- `priority`  
  Relative ordering hint for early versions of question selection. Lower numbers can be treated as higher priority, or the team can define another simple convention as long as it is consistent.

- `enabled`  
  Boolean flag for whether the question is active.

## Answer Values

User answers must be constrained to:

- `yes`
- `probably_yes`
- `i_dont_know`
- `probably_no`
- `no`

## Notes

- Entity attributes should stay simple and mostly boolean in the MVP.
- Questions should map cleanly to one primary attribute.
- New attributes and questions can be added in later schema versions without changing the basic shape.
