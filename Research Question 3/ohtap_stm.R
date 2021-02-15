library(stm)
library(ggplot2)
library(tidyverse)
library(tidytext)

stm_all <- function(input) {
  sub = read.csv(input)
  print(head(sub))
  print(nrow(sub))
  custom <- "\U0001f604\U0001f604\U0001f604|???|??????|\U0001f631\U0001f631\U0001f631\U0001f631\U0001f631|\U0001f4a4\U0001f4a4\U0001f4a4|\U0001f319\U0001f306|\U0001f1ee\U0001f1f9|\U0001f496|???|???|\U0001f33b|???|??????|\U0001f4aa\U0001f4aa\U0001f4aa|\U0001f697|\U0001f494|\U0001f64f\U0001f64f\U0001f64f\U0001f64f\U0001f4aa\U0001f4aa\U0001f4aa\U0001f47c\U0001f47c\U0001f47c\U0001f478\U0001f478\U0001f478\U0001f48b\U0001f48b\U0001f48b\U0001f48b|???|???|???|???|???|@|???|???|\U0001f618\U0001f40e\U0001f378|\U0001f493|???|???|??|???|???|???|???|\U0001f614\U0001f614\U0001f614\U0001f614|???|??|?????????|???|???|??|???|???|??????|???|??|???|???|???|??|???|???|??????|???|??????|??????|??????|??????|????|??|????|+|?????????|??????|?????????|?????????|~~~~~|+|???\n"
  print("Start processing")
  processed <- textProcessor(documents = sub$Event.extents, metadata = sub, wordLengths = c(2,Inf), stem=F, removenumbers = TRUE, removepunctuation = TRUE, custompunctuation = custom, verbose = FALSE)
  save(processed, file="~/Downloads/processed_ohtap.RData")
  print("Start prepping")
  documents <- prepDocuments(processed$documents, processed$vocab, processed$meta, lower.thresh=20)
  save(documents, file="~/Downloads/documents_ohtap.RData")
  print("Start stming")
  stm.out <- stm(documents$documents, documents$vocab, K=10, data=documents$meta)
  save(stm.out, file="~/Downloads/stm_ohtap.RData")
}

stm_all("~/Downloads/Winter Quarter/OHTAP/event_extents.csv")

visualize_topic <- function(filename) {
  load(filename)
  topic_model = stm.out
  td_beta <- tidy(topic_model)
  td_beta %>%
    group_by(topic) %>%
    top_n(10, beta) %>%
    ungroup() %>%
    mutate(topic = paste0("Topic ", ifelse(topic < 10, paste0("0", topic, sep=""), topic)),
           term = reorder_within(term, beta, topic)) %>%
    ggplot(aes(term, beta)) + 
    geom_col(alpha = 0.8, show.legend = FALSE) +
    facet_wrap(~ topic, scales = "free_y") +
    coord_flip() +
    scale_x_reordered()
}
visualize_topic("~/Downloads/stm_ohtap.RData")

load("~/Downloads/processed_ohtap.RData")
load("~/Downloads/documents_ohtap.RData")
load("~/Downloads/stm_ohtap.RData")
# visualize topic change across years
all_documents_topics = stm.out$theta
# find the most likely topic
likely_topics = matrix(nrow = nrow(all_documents_topics), ncol = 4) # year, top 3 topics


# ===================== get year in metadata


topics_by_year = matrix(data = 0, nrow = , ncol = 20) # year, topic
for (i in 1:nrow(all_documents_topics)) {
  likely_topics[i, 1] = documents$meta$year[i]
  top_three_indices = order(all_documents_topics[i,], decreasing = TRUE)[1:3]
  for (j in 1:3) {
    likely_topics[i, j + 1] = top_three_indices[j]
    year = documents$meta$year[i]
    topics_by_year[year - 1945, top_three_indices[j]] = topics_by_year[year - 1945, top_three_indices[j]] + 1
  }
}
likely_topics
head(likely_topics)
topics_by_year = as.data.frame(topics_by_year)
years = seq(1946, 2019, by = 1)

ggcorrplot(stm.out_200000$sigma) # need to realign

high_prob_words = labelTopics(stm.out_200000)$prob
high_prob_words = as.data.frame(high_prob_words)
write_csv(high_prob_words, "~/Downloads/high_prob_words.csv")

topic_words = labelTopics(stm.out_200000, n = 20)$prob
topic_words = as.data.frame(topic_words)
topic_words

all_words = c()
for(i in 1:20) {
  var = paste("")
}

# plot each one
plot_list = list()
for(i in 1:50) {
  text = paste(paste(high_prob_words[i, ], collapse = ","))
  grob = grobTree(textGrob(text, x=0.1,  y=0.95, hjust=0,
                           gp=gpar(col="red", fontsize=13, fontface="italic")))
  p = ggplot() + geom_line(aes(x = years, y = topics_by_year[[paste("V", i, sep = "")]])) + annotation_custom(grob) + ylab("topic count")
  plot_list[[i]] = p
}
