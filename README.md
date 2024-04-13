# recommendation
旅游推荐系统；实现一个旅游推荐算法并做一个系统展示出来

## 数据集
- 本算法采用的是Foursquare个人签到数据。Foursquare个人签到数据集是一个公开的数据集，包含了Foursquare社交媒体平台上用户的签到记录。该数据集包含了来自全球的用户签到数据，包括签到的地点、时间、用户ID等信息。这些数据可以用于研究用户行为、地理位置分析、社交网络分析等领域。
- 主要有4个数据文件users.dat,venues.dat,ratings.dat,checkins.dat

## 算法思路
> 本算法主要是分为三部分：群组划分、主题建模、地点推荐。群组划分采用的是K-Means聚类算法实现，地点主题建模采用LDA主题模型进行构建。地点推荐采用了前两步的数据进行实现。

![image](https://github.com/sichenyong/recommendation/assets/91589693/37ee23f4-284e-45ce-9761-f54de1f234ee)

## TCM模型
在介绍TCM模型前，先介绍以下TCM模型的参数，
![image](https://github.com/sichenyong/recommendation/assets/91589693/6859f4d0-7da0-41c1-8190-6b53abdf04f1)

TCM模型基于三种考虑：
1)	不同的旅游群组喜欢不同的景点，有的喜欢自然景观类的，有人喜欢现象级的。TCM模型将景点类型作为潜在主题。
2)	群组选择旅游景点还受成本因素的影响，对于某个群组，即便是某个景点风评很好，景观也很美丽，但是消费却非常高，这个群组也未必会选择该景点作为访问。
3)	群组是否选择旅游景点同样受评分的影响，评分是最直接、直观的给用户带来感觉的影响因素，因此本模型还融入了评分因素的影响。

|   TCM：基于潜在主题及成本的推荐   |
| ---- |
|   Input: User_id, Top-N,表3.7中的其他数据|
| Output: Top-N地点|
|1.	根据输入获取用户群组以及群组的历史访问记录|
|2.	获取群组访问的主题信息以及频次|
|3.	获取对应主题下的地点数|
|4.	获取用户对这些地点的成本数据|
|5.	获取群组对这些地点的评分数据|
|6.	综合上述数据获取每个地点对应的综合结果|
|7.	根据综合结果排序，获取Top-N个地点信息|
## 算法结果
![image](https://github.com/sichenyong/recommendation/assets/91589693/7fcb5c9d-2fa7-494e-9002-8fcfb2bbb3f4)

## 网站效果
![image](https://github.com/sichenyong/recommendation/assets/91589693/6c9bf599-22a0-440b-a11b-06ef5479568a)
![image](https://github.com/sichenyong/recommendation/assets/91589693/df29cc71-7c6a-4b28-b46c-5faabb3a2771)

![image](https://github.com/sichenyong/recommendation/assets/91589693/f145a333-6d20-4838-8eb2-9e43d216d57f)
![image](https://github.com/sichenyong/recommendation/assets/91589693/cdbc4b92-4596-43c2-bc52-7e17a6e08568)






