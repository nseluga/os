---
topic: google-maps-places-autocomplete
updated: 2026-07-25
sources: [https://github.com/visgl/react-google-maps/issues/736, https://developers.google.com/maps/legacy, https://developers.google.com/maps/documentation/javascript/load-maps-js-api, https://developers.google.com/maps/documentation/javascript/error-messages, https://developers.google.com/maps/documentation/javascript/places-migration-autocomplete, https://developers.google.com/maps/documentation/javascript/examples/place-autocomplete-element]
---
## Recommendation
Diagnose before fixing: check console for the literal string "is not available to new customers". If present → hard per-Cloud-project gate, migrate to `google.maps.places.PlaceAutocompleteElement` (no loading tweak fixes it). If absent → minimal fix is add `loading=async` to the script URL and `await google.maps.importLibrary("places")` before instantiating `Autocomplete`, because the outer script's `load`/Next `Script onLoad` event can fire before `google.maps.places` is populated.

## Rejected Alternatives
- `callback=` global-function pattern — still supported, but `importLibrary()` is Google's current recommendation and composes better with React effects.
- `@googlemaps/js-api-loader` / `useLoadScript` wrapper libs — unnecessary new dependency; the native fix is a few lines.

## Version / Deprecation / CVE Notes
- March 1 2025 cutoff: `google.maps.places.Autocomplete` + `AutocompleteService` (JS widget classes) blocked for any Cloud project with no prior Places API usage before that date. This is a project-history gate on the JS surface specifically — independent of API key restrictions and independent of whether legacy REST (`/place/autocomplete/json`) is enabled and returning results. A key can serve legacy REST fine while the JS widget is gated.
- Pre-cutoff/existing projects: `Autocomplete` keeps working, gets bug fixes for major regressions only, 12+ months notice promised before hard removal.
- No CVE. `loading=async` warning is cosmetic/perf, not a functional error: "Google Maps JavaScript API has been loaded directly without loading=async. This can result in suboptimal performance."

## Integration Notes
- Add `loading=async` to `maps/api/js?key=...&libraries=places&loading=async`. Without it, `libraries=places` still resolves via an internal async import even though the outer `<script>` load event fires on the bootstrap script loading, not on `google.maps.places` being populated — this is the race that produces "sometimes works in dev, silently no dropdown in prod."
- Correct init shape: inside onLoad/effect, `const {Autocomplete} = await google.maps.importLibrary("places")` then `new Autocomplete(inputRef.current, {...})` — not a bare `new google.maps.places.Autocomplete(...)` assumed-ready at top of onLoad.
- `PlaceAutocompleteElement` is a Web Component appended to the DOM (`document.body.appendChild(el)` or via a container ref) — it is NOT attached to an existing `<input ref>`, biggest structural break for ref-based React code. Listen for `gmp-select`, not `place_changed`.
- Field mapping: `place.formatted_address` → `await place.fetchFields({fields:['formattedAddress','location']})` then `place.formattedAddress`; `place.geometry.location.lat()/.lng()` → `place.location.lat()/.lng()` (same LatLng object/methods, new camelCase property path, no `geometry` wrapper).
- Error strings to distinguish root cause: `ApiNotActivatedMapError` (Maps JS API not enabled on project), `ApiTargetBlockedMapError` (key's API restrictions exclude this API), `InvalidKeyMapError` (key missing/malformed/not yet propagated), `RefererNotAllowedMapError` (HTTP-referrer restriction blocks this origin). None of these overlap with the new-customer gating string — check both independently, symptom (no dropdown) is identical for all.
