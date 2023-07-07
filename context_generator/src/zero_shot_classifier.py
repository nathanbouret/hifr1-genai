# from transformers import pipeline
# import pickle

# def zero_shot_classification(chunks, classes_poi, threshold=0.8):

#     classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli") 
#     # class_poi = ["challenge", "investment", "achievement", "innovation", "best practice", "ressource"]
#     dict_poi = {}
#     counter = 0
#     for num_chunk, chunk in enumerate(chunks):
#         # print(num_chunk)
#         if counter%200==0:
#             print(f'*********************** zero_shot_classification step:{counter} ***********************')
#         chunk_text = chunk.page_content
#         classif = classifier(chunk_text, classes_poi, multi_label=True)
#         for i in range(len(classif['scores'])):
#             score = classif['scores'][i]
#             if score >= threshold:
#                 label = classif['labels'][i]
#                 if label in dict_poi:
#                     dict_poi[label].append((chunk_text, score, num_chunk))
#                 else:
#                     dict_poi[label]=[]
#                     dict_poi[label] = [(chunk_text, score, num_chunk)]
#         counter = counter + 1

#     with open('chunks_zero_shot_classification.p', 'wb') as handle:
#         pickle.dump(dict_poi, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     return dict_poi