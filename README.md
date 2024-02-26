# EC530_ML

**API MODULES**  
Authentication/Authorization:
- post new user
- post token
- get token
- delete user
  
Data Upload:
- post new project  
- get image from project
- post label/class data  
- delete image  
- put new image into project

Data Analysis:
- post analysis

Training:
- add/remove training points  
- change parameters  
- start/stop training  
- restart training  
- get status of training  
- get results  
  
Model Publishing:
- post model
- get model
- delete model

Inference:
- post inference
- get inference
- delete inference

Test Model:
- post run tests
- get results

Reports:
- post reports
- get reports
- delete reports

**Database Schema**
Users:
- user id
- name

Projects:
- project id
- user id
- name
- created
- last update

Dataset:
- data id
- project id

Model:
- model id
- 
