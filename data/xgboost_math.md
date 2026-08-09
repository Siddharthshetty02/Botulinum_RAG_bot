# Mathematical Formulation of Smart Physiotherapy Rehab System using XGBoost 

## **1 Raw Sensor Input (Time Series)** 

From the IMU device (MPU6050), the raw signal at time _t_ is: 



where: 

- _ax, ay, az_ represent linear acceleration 

- _gx, gy, gz_ represent angular velocity 

The full dataset is a time series: 



## **2 Sensor Fusion and Angle Computation** 

To convert raw IMU data into joint angle, a complementary filter is used: 



where: 



- _gt_ is gyroscope reading 



Thus, we obtain the angle signal: 



1 

## **3 Feature Extraction** 

From the angle signal _θ_ ( _t_ ), the following features are computed: 

### **3.1 Range of Motion** 

_ROM_ = max( _θ_ ) _−_ min( _θ_ ) 

### **3.2 Angular Velocity** 





### **3.3 Stability (Variance)** 



### **3.4 Jerk (Smoothness)** 



### **3.5 Time per Repetition** 



### **3.6 Final Feature Vector** 



## **4 XGBoost Model** 

### **4.1 Prediction Function** 

The final prediction is computed as: 



where: 

2 

- _fk_ is the _k_ -th decision tree 

- _K_ is the total number of trees 

### **4.2 Tree Function** 

Each tree maps input to a leaf weight: 



where: 

- _q_ ( **x** ) is the leaf index 

• _w_ is the leaf weight 

### **4.3 Multi-class Classification (Softmax)** 



## **5 Objective Function** 

The model minimizes: 



where: 

- _l_ is the loss function (e.g., log loss) 

- Ω( _f_ ) is the regularization term 

### **5.1 Regularization** 



where: 

- _T_ is number of leaves 

• _w_ are leaf weights 

3 

## **6 End-to-End Mathematical Flow** 

_Xt → θ_ ( _t_ ) 

_θ_ ( _t_ ) _→_ **x** 





## **7 Key Insight** 

Time Series _→_ Feature Engineering _→_ Tabular ML 

XGBoost does not operate directly on raw sensor signals; instead, it relies on structured numerical features derived from the signal. 

## **8 References** 

## **References** 

- [1] T. Chen and C. Guestrin, “XGBoost: A Scalable Tree Boosting System,” _Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD)_ , 2016. [Online]. Available: `https://arxiv.org/abs/1603.02754` 

- [2] Wearable Sensor-Based Rehabilitation Exercise Assessment. [Online]. Available: `https: //www.researchgate.net/publication/273953220` 

4 

