library(shiny)
library(rvest)
library(dplyr)
library(ggplot2)

# Function to scrape player data
scrape_player_data <- function(url) {
  player_stats <- url %>%
    read_html() %>%
    html_nodes(xpath = '//*[@id="top"]/div[4]/div/div[1]/div[1]/div[2]/div[1]/div[1]/table') %>%
    html_table(fill = TRUE) %>%
    as.data.frame()
  return(player_stats)
}

# UI
ui <- fluidPage(
  titlePanel("Sachin Tendulkar vs Virat Kohli: Runs Comparison"),
  sidebarLayout(
    sidebarPanel(
      selectInput("format", "Select Format:", choices = c("Test", "ODI", "T20I", "IPL"), selected = "Test")
    ),
    mainPanel(
      plotOutput("stacked_bar_chart")
    )
  )
)

# Server
server <- function(input, output) {
  # Render the stacked bar chart
  output$stacked_bar_chart <- renderPlot({
    # Scrape data for Sachin Tendulkar
    url_sachin <- "https://www.cricbuzz.com/profiles/25/sachin-tendulkar"
    df_sachin <- scrape_player_data(url_sachin)
    
    # Scrape data for Virat Kohli
    url_virat <- "https://www.cricbuzz.com/profiles/1413/virat-kohli"
    df_virat <- scrape_player_data(url_virat)
    
    # Filter data for the selected format
    sachin_data <- df_sachin[df_sachin$X1 == input$format, ]
    virat_data <- df_virat[df_virat$X1 == input$format, ]
    
    # Check if data is available for the selected format
    if (nrow(sachin_data) == 0 || nrow(virat_data) == 0) {
      cat("Data not available for the selected format.")
      return(NULL)
    }
    
    # Get the column names excluding 'X1'
    attributes <- colnames(sachin_data)[-1]
    
    # Extract Sachin and Virat's runs
    sachin_runs <- as.numeric(sachin_data[2, -1])
    virat_runs <- as.numeric(virat_data[2, -1])
    
    # Calculate the total runs for each attribute
    total_runs <- sachin_runs + virat_runs
    
    # Calculate the percentage of runs contributed by each player
    sachin_percentage <- (sachin_runs / total_runs) * 100
    virat_percentage <- (virat_runs / total_runs) * 100
    
    # Create a data frame for plotting
    df <- data.frame(
      Attributes = attributes,
      Sachin_Tendulkar = sachin_percentage,
      Virat_Kohli = virat_percentage
    )
    
    # Reshape data for plotting
    df_long <- pivot_longer(df, cols = c(Sachin_Tendulkar, Virat_Kohli), names_to = "Player", values_to = "Percentage")
    
    # Create the stacked bar chart
    stacked_bar_chart <- ggplot(df_long, aes(x = Percentage, y = Attributes, fill = Player)) +
      geom_bar(stat = "identity", position = "stack") +
      labs(title = paste("Comparison of", input$format, "Runs: Sachin Tendulkar vs Virat Kohli"),
           x = "Percentage of Total Runs", y = "Attributes") +
      theme_minimal() +
      theme(axis.text.y = element_text(size = 10))
    
    return(stacked_bar_chart)
  })
}

# Run the application
shinyApp(ui = ui, server = server)
