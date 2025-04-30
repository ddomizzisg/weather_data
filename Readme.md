# Set of functions to process weather data

```mermaid
flowchart TD
    group_by_state-->clustering
    clustering-->regressions
    clustering-->mapping
    regressions-->forecasting
```