# Define the partial derivative functions
fx <- function(x, y) {
  3 * x^2 - 3
}

fy <- function(x, y) {
  2 * y - 6
}

# Evaluate the partial derivatives at the point (-1, 3)
fx_value <- fx(-1, 3)
fy_value <- fy(-1, 3)

# Print the results
print(paste("fx(-1, 3) =", fx_value))
print(paste("fy(-1, 3) =", fy_value))
