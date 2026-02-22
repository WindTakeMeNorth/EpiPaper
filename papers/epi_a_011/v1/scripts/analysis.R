# epi_a_011 - School Catchment Redesign and Pediatric Obesity Trajectories
# Auto-generated starter script for EPI-APE.

suppressPackageStartupMessages({
  library(data.table)
  library(fixest)
  library(ggplot2)
})

cat("Running analysis for epi_a_011\n")

# TODO: Replace with real data extraction code.
dt <- data.table(
  unit = rep(1:200, each = 8),
  year = rep(2018:2025, times = 200),
  treated = rep(sample(c(0, 1), 200, replace = TRUE), each = 8)
)

dt[, post := as.integer(year >= 2022)]
dt[, y := 0.5 * treated * post + rnorm(.N)]

mod <- feols(y ~ treated * post | unit + year, data = dt, vcov = ~unit)
print(summary(mod))

out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
fwrite(data.table(term = names(coef(mod)), estimate = as.numeric(coef(mod))), file.path(out_dir, "main_estimates.csv"))

png(file.path(out_dir, "event_plot.png"), width = 800, height = 500)
plot(dt$year, dt$y, pch = 19, col = rgb(0, 0, 0, 0.15), main = "Placeholder outcome path")
dev.off()

cat("Done. Outputs in ./outputs\n")
