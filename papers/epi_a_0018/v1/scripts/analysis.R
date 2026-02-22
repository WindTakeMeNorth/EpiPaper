# epi_a_0018 - Mobile Vaccine Campaign and Outbreak Response Delay in Border Municipalities
# Reproducible baseline analysis for EPI-APE.

suppressPackageStartupMessages({
  library(data.table)
  library(fixest)
  library(jsonlite)
})

cat("Running analysis for epi_a_0018\n")

input_path <- "data/panel.csv"
if (!file.exists(input_path)) {
  stop("Missing input dataset data/panel.csv. Add real data before running.")
}

dt <- fread(input_path)

required_cols <- c("unit", "year", "outcome", "treated", "post")
missing_cols <- setdiff(required_cols, names(dt))
if (length(missing_cols) > 0) {
  stop(paste("Dataset missing required columns:", paste(missing_cols, collapse = ", ")))
}

mod <- feols(outcome ~ treated * post | unit + year, data = dt, vcov = ~unit)
print(summary(mod))

out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
fwrite(data.table(term = names(coef(mod)), estimate = as.numeric(coef(mod))), file.path(out_dir, "main_estimates.csv"))

es <- feols(outcome ~ i(year, treated, ref = min(year)) | unit + year, data = dt, vcov = ~unit)
event_dt <- data.table(term = names(coef(es)), estimate = as.numeric(coef(es)))
fwrite(event_dt, file.path(out_dir, "event_study.csv"))

spec_log <- list(
  paper_id = "epi_a_0018",
  model = "TWFE with clustered SE",
  rows = nrow(dt),
  units = uniqueN(dt$unit),
  years = paste(range(dt$year), collapse = "-")
)
writeLines(toJSON(spec_log, auto_unbox = TRUE, pretty = TRUE), file.path(out_dir, "specification_log.json"))

cat("Done. Outputs in ./outputs\n")
