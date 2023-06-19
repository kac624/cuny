library(cowplot)

#### Full Plot Grid

create_plot <- function(category, variable) {
  xl <- readxl::read_excel('data/DATA624_Project1_Data_Schema.xlsx',
                           sheet = category, skip = 2)
  series <- xl[1:1622,variable]
  series <- ts(deframe(series), frequency = 1)

  plot <- ggplot(fortify(series), aes(x,y)) + 
    geom_line() +
    theme(axis.title.x = element_blank(),
          axis.title.y = element_blank())

  return(plot)
}

combos <- list(c('S01', 'Var01'),
               c('S01', 'Var02'),
               c('S02', 'Var02'),
               c('S02', 'Var03'),
               c('S03', 'Var05'),
               c('S03', 'Var07'),
               c('S04', 'Var01'),
               c('S04', 'Var02'),
               c('S05', 'Var02'),
               c('S05', 'Var03'),
               c('S06', 'Var05'),
               c('S06', 'Var07'))

plot_list <- list()
for (combo in combos) {
  plot <- create_plot(combo[1],
                      combo[2])
  name <- paste0(combo[1],combo[2])
  plot_list[[name]] <- plot
}

plot_grid(plotlist = plot_list, nrow = 3, ncol = 4)

### Baseline Example

p1 <- autoplot(naive_model) + 
  autolayer(test, alpha = 0.5) +
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.position = "none")

p2 <- autoplot(mean_model) + 
  autolayer(test, alpha = 0.5) +
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.position = "none")

p3 <- autoplot(ets_forecast) + 
  autolayer(test, alpha = 0.5) +
  theme(axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        legend.position = "none")

plot_grid(p1, p2, p3, nrow = 3)
