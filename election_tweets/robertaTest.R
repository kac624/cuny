reticulate::py_install('transformers', pip = TRUE)

library(keras)
library(tensorflow)
library(dplyr)
library(tfdatasets)
transformer = reticulate::import('transformers')
