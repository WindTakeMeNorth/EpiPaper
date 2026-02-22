suppressPackageStartupMessages({
  library(data.table)
  library(fixest)
  library(jsonlite)
})

set.seed(20260222)

message("Running manual-mode Round 1 analysis for epi_a_0019")

required_files <- c(
  "data/panel.csv",
  "data/border_exposure.csv"
)

missing_files <- required_files[!file.exists(required_files)]
if (length(missing_files) > 0) {
  stop(paste("Missing required input file(s):", paste(missing_files, collapse = ", ")))
}

panel <- fread("data/panel.csv")
border <- fread("data/border_exposure.csv")

required_panel_cols <- c(
  "county_fips",
  "state_fips",
  "year",
  "amenable_mortality_25_64",
  "allcause_mortality_25_64",
  "population_25_64",
  "nonexp_state"
)

required_border_cols <- c(
  "county_fips",
  "adjacent_expansion_year",
  "is_border_county",
  "commuting_share_crossborder"
)

missing_panel <- setdiff(required_panel_cols, names(panel))
missing_border <- setdiff(required_border_cols, names(border))

if (length(missing_panel) > 0) {
  stop(paste("panel.csv missing columns:", paste(missing_panel, collapse = ", ")))
}
if (length(missing_border) > 0) {
  stop(paste("border_exposure.csv missing columns:", paste(missing_border, collapse = ", ")))
}

dt <- merge(panel, border, by = "county_fips", all.x = TRUE)
dt <- dt[nonexp_state == 1]

dt[, treated_border := as.integer(is_border_county == 1 & !is.na(adjacent_expansion_year))]
dt[, event_time := year - adjacent_expansion_year]
dt[, state_year := paste0(state_fips, "_", year)]

# Keep a symmetric event window to avoid long-tail leverage.
dt <- dt[(is.na(event_time)) | (event_time >= -6 & event_time <= 6)]

# Main event-study model
mod_event <- feols(
  amenable_mortality_25_64 ~ i(event_time, treated_border, ref = -1) |
    county_fips + state_year,
  data = dt,
  weights = ~population_25_64,
  vcov = ~state_fips
)

event_out <- data.table(
  term = names(coef(mod_event)),
  estimate = as.numeric(coef(mod_event)),
  se = as.numeric(se(mod_event))
)

# TWFE post indicator summary model
dt[, post_exposure := as.integer(!is.na(event_time) & event_time >= 0)]
mod_twfe <- feols(
  amenable_mortality_25_64 ~ treated_border * post_exposure |
    county_fips + state_year,
  data = dt,
  weights = ~population_25_64,
  vcov = ~state_fips
)

twfe_out <- data.table(
  term = names(coef(mod_twfe)),
  estimate = as.numeric(coef(mod_twfe)),
  se = as.numeric(se(mod_twfe))
)

# Placebo: shift policy timing three years earlier
dt[, placebo_event_time := year - (adjacent_expansion_year - 3)]
dt <- dt[(is.na(placebo_event_time)) | (placebo_event_time >= -6 & placebo_event_time <= 6)]

mod_placebo <- feols(
  amenable_mortality_25_64 ~ i(placebo_event_time, treated_border, ref = -1) |
    county_fips + state_year,
  data = dt,
  weights = ~population_25_64,
  vcov = ~state_fips
)

placebo_out <- data.table(
  term = names(coef(mod_placebo)),
  estimate = as.numeric(coef(mod_placebo)),
  se = as.numeric(se(mod_placebo))
)

out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

fwrite(event_out, file.path(out_dir, "main_event_study.csv"))
fwrite(twfe_out, file.path(out_dir, "main_twfe.csv"))
fwrite(placebo_out, file.path(out_dir, "robust_placebo.csv"))

spec_log <- list(
  paper_id = "epi_a_0019",
  version = "v2",
  models = c("event-study", "twfe", "placebo-event-study"),
  cluster_level = "state_fips",
  n_rows = nrow(dt),
  n_counties = uniqueN(dt$county_fips),
  year_min = min(dt$year),
  year_max = max(dt$year),
  treated_counties = sum(unique(dt[, .(county_fips, treated_border)])$treated_border == 1)
)

writeLines(
  toJSON(spec_log, auto_unbox = TRUE, pretty = TRUE),
  file.path(out_dir, "specification_log.json")
)

message("Analysis complete. Outputs written to ./outputs")
