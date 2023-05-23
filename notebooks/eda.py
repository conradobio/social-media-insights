import pandas as pd
import json

with open('./data/ic-sjcampos/ic-sjcampos-posts-2023-05-21.json', 'r') as f:
        data = json.load(f)

# for i, post in enumerate(data):
#     link_post = post['shortCode']
#     tipo = post['type']
#     data_postagem = post['timestamp']
#     qtd_comments = post['commentsCount']
#     qtd_likes = post['likesCount']
#     legenda = post['caption']
#     hashtags = post['hashtags']

    # posts_stats.append(dict(uid=link_post,
    #                         tipo=tipo,
    #                         data_postagem=data_postagem, 
    #                         legenda=legenda,
    #                         qtd_likes=qtd_likes,
    #                         qtd_comments=qtd_comments,
    #                         hashtags=hashtags,
    #                         data_extracao=date
    #                         ))

#print(len(data[24]['relatedProfiles']))
#print(data[24].keys())
print(len(data[24]['latestIgtvVideos']))