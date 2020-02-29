### 实体类型

|  实体类型  | 中文含义 | 实体数量 | 举例 |
| ---------- | -------- | -------- | ---- |
|  Disease   |   疾病   |          |      |
| Department |   科室   |          |      |
|   Check    | 检查项目 |          |      |
|    Drug    | 治疗药品 |          |      |
|    Food    |   食物   |          |      |
|  Symptom   |   症状   |          |      |
|   Doctor   |   医生   |          |      |


### 可能的关系
* <Disease,belongs_to,Department> 疾病所属科室
* <Disease,inspection_item,Check> 疾病检查项目
* <Disease,common_drug,Drug> 疾病常用药物
* <Disease,has_symptom,Symptom> 疾病症状
* <Disease,recommand_doctor,Doctor> 疾病推荐医生
* <Disease,good_food,Food>
* <Disease,avoid_food,Food>
* <Disease,recommand_recipes,Food>
* <Disease,has_complication,Symptom>

### 实体关系

|   实体关系类型    | 中文含义 | 关系数量 | 举例 |
| ----------------- | -------- | -------- | ---- |
|    belongs_to     |   属于   |          |      |
|    common_drug    | 常用药物 |          |      |
|     good_food     | 宜吃食物 |          |      |
|    avoid_food     | 忌吃食物 |          |      |
|    check_item     | 检查项目 |          |      |
| recommand_recipes | 推荐食谱 |          |      |
| has_complication  |  并发症  |          |      |
|    has_symptom    | 疾病症状 |          |      |
| recommand_doctor  | 推荐医生 |          |      |
|                   |          |          |      |

### Disease properties

|      属性类型      |   中文含义   | 举例 |
| ------------------ | ------------ | ---- |
|        name        |   疾病名称   |      |
|        desc        |   疾病描述   |      |
|       cause        |   疾病病因   |      |
|      prevent       |   预防措施   |      |
|    treat_cycle     |   治疗周期   |      |
|     treat_way      |   治疗方式   |      |
|     cure_prob      |   治愈概率   |      |
| susceptible_people |   易感人群   |      |
| medical_insurance  | 是否医保疾病 |      |
|   disease_ratio    |   患病比例   |      |
|  transmission_way  |   传染方式   |      |
|     treat_cost     |   治疗费用   |      |
|      nursing       |   护理方法   |      |


### 实现思路
* **图谱构建**
数据爬取-->数据预处理-->实体类型构建-->关系类型构建-->创建neo4j数据
* **问题解析:**
 自然语言查询-->意图识别(Intention Recognition)-->实体识别-->实体链接(Entity Linking)+关系识别(Relation Detection) -->查询语句拼装(Query Construction)-->返回结果选择(Answering Selection)
 * **意图识别:**
 常用的有：
  1：基于词典模板的规则分类
  2：基于过往日志匹配（适用于搜索引擎）
  3：基于分类模型进行意图识别(CNN,RNN,MachineLearning)
  我们采用的是基于词典模板的规则分类方法，意图对应项目中的question_type。

  * **实体链接:**

### 技术路线
    * 前端 ： html、css、jQuery、ajax、bootstrap4
    * 后端 : Flask、neo4j、scrapy