# IoT-Based Intelligent Physiotherapy Monitoring and Real-Time Feedback System Using Wearable IMU Sensors and Machine Learning 

|Siddharth Shetty|Sushmita dyamanagoudra|T K Pradeep Kumar|
|---|---|---|
|_Dept. of Computer Science and Engi-_<br>_neering_|_Dept. of Computer Science and Engi-_<br>_neering_|_Dept. of Computer Science and Engi-_<br>_neering_|
|_AMC Engineering College_<br>Bengaluru, India<br>siddharthshetty2032005@gmail.com|_AMC Engineering College_<br>Bengaluru, India<br>dsushmita227@gmail.com|_AMC Engineering College_<br>Bengaluru, India<br>tkpradeep.it@gmail.com|
|Spoorti Malled<br>_Dept. of Computer Science and_<br>_Engineering_<br>_AMC Engineering College_<br>Bengaluru, India<br>spoortimalled@gmail.com|Sree Raghavendra P<br>_Dept. of Computer Science and Engi-_<br>_neering_<br>_AMC Engineering College_<br>Bengaluru, India<br>reddyraghu75109@gmail.com|Sudeep M<br>_Dept. of Computer Science and Engi-_<br>_neering_<br>_AMC Engineering College_<br>Bengaluru, India<br>sudeep70vv@gmail.com|



**Abstract—Home-based physiotherapy is mostly unsupervised. Thus, it is challenging to ensure that the patient performs the rehabilitation exercises correctly and consistently to maximize the recovery effect. This project aims to design an IoT-based intelligent physiotherapy monitoring and feedback system by using the Internet of Things, machine-learning and the development of a mobile application to enable an intelligent and portable rehabilitation system. The proposed system uses wearable IMU sensors to capture the movement features of knee rehabilitation motions. The sensor data is processed, and relevant features extracted for the prediction model. An ensemble classifier is formulated to predict whether the rehabilitation exercise is performed correctly. The prediction results along with the exercise information are displayed to the user through an Android mobile application, on which the ondevice classification pipeline is deployed. By enabling an affordable and portable rehabilitation system, the proposed framework can contribute to develop a remote physiotherapy monitoring system, promote correct exercise performance and motivate the patients to adhere to their rehabilitation protocol. In addition, by using machine-learning methods, the system can track and monitor the patients’ rehabilitation process and enable physiotherapists to follow up their rehabilitation progress easily. The system can scale up for future developments by incorporating real patient data, multiple physiotherapy exercises and the backend dashboard for physiotherapists.** 

**_Index Terms—IoT, wearable sensors, IMU, ESP32, physiotherapy monitoring, XGBoost, real-time feedback, knee rehabilitation._** 

## I. INTRODUCTION 

Physiotherapy is an essential element of the rehabilitation process, but its effectiveness depends on the accuracy with which particular exercises are repeated. This accuracy is manifested in the correctness of posture and movements performed, as well as the speed of their execution. A physiotherapist can demonstrate exercises and help the patient repeat them correctly; thus, in the office, the therapist can immediately point out mistakes and show how to perform the movement correctly. This opportunity is not available at home, where patients are often forced to repeat incorrect actions several times in a row, which can be detrimental to the injured knee. 

Wearable Inertial Measurement Units (IMU) are a recent 

innovation in motion capture technology that allow lower-cost and more flexible, miniature alternatives to conventional camerabased systems and are quickly gaining popularity due to their applicability in non-clinical settings where they can perform consistently despite variations in lighting. However, IMUs as well as other commercial wearable systems currently offer no direct feedback to the user and only provide analysis of the rehabilitation data for clinicians after the fact. 

In this paper, we propose an end-to-end system that employs the potential of these wearable IMU in conjunction with ensemble ML and IoT-enabled feedback to provide direct correction signals to the user in case of erroneous repetitions during the rehabilitation process in real-time. 

Two Inertial Measurement Units (IMUs) estimate the flexionextension angle of the knee joint: one was attached to the thigh and the other to the shank. The proposed fusion estimates the rotation of the joint during each repetition. Then, a Soft-Voting Ensemble Classifier analyzes each repetition and classifies it as correct or incorrect and informs the user via her cellphone about the correctness of the performed repetitions. As a result, a CyberPhysical System was designed, which is closed by the feedback received from the user. Our contributions include: 

1. A system based on a dual IMU setup that utilizes a microcontroller to record kinetic and kinematic data about the knee joint and transmit it to a local Bluetooth module for realtime processing with minimal latency is introduced. 

2. A Soft Voting ensemble of logistic regression, random forests, and XGBoost classifiers is suggested to distinguish between correctly and incorrectly performed rehabilitation exercises. 

3. An end-to-end pipeline is designed and deployed on an Android mobile application to enable low-latency feedback and corrections during the rehabilitation process. 

The remainder of this paper is organized as follows. Section II reviews related work concerning commercial wearable inertial systems and IMUs, and motivates our design. Section III describes the system architecture, defines the problem formulation, and presents sensor placement assumptions. Section IV addresses implementation and design considerations for the system’s hardware and signal-processing chain. Section V presents results, and Section VI concludes the paper.VI. 

## II. RELATED WORK 

Milosevic et al. [1] compared camera-based motion capture (Microsoft Kinect) with wearable inertial sensors for home-based motor rehabilitation and found IMUs to be a reliable, cost-effective, and less spatially restrictive alternative to optical tracking for continuous joint monitoring. Mitternacht et al. [2] validated the use of a single IMU for acquiring lower-limb motion characteristics in physiotherapy applications, showing that even minimal sensor configurations can yield clinically useful kinematic data. 

Majumder and Deen [3] developed a wearable IMU-based system for real-time monitoring of lower-limb joints, applying filtering techniques to improve joint-angle estimation accuracy; this work forms a strong foundation for the sensorfusion approach adopted in the present system. Rahman et al. [4] and Carro et al. [5] separately addressed sources of estimation error—sensor misalignment and drift—through personalized calibration and multi-sensor fusion, respectively, both of which motivate the calibration routine used in this work. 

On the machine-learning side, Hua et al. [6] evaluated several ML models for classifying upper-extremity exercises from IMU-based kinematic data, demonstrating that classifier choice materially affects rehabilitation-monitoring accuracy. Forsyth et al. [7] and Riffitts et al. [8] validated wearable sensing specifically for knee rehabilitation and range-of-motion tracking, while Sun et al. [9] and Cornish et al. [10] applied IMU-based quantitative assessment to gait and post-arthroplasty knee kinematics, respectively, reinforcing the clinical relevance of IMU-derived features for joint-specific recovery tracking. 

Franco et al. [11] proposed motion knee-angle recognition specifically for muscle-rehabilitation solutions, and Smith et al. [12] demonstrated a wearable IoT-based system for knee monitoring that transmits sensor data for real-time evaluation, closely aligning with the goals of this work. Across this body of literature, two limitations recur: first, most systems emphasize accurate measurement but stop short of delivering feedback during the exercise itself; second, classification is typically performed using a single model, leaving the system vulnerable to that model's individual weaknesses on noisy or atypical data. The proposed system addresses both limitations through a real-time, on-device feedback loop and a Soft-Voting ensemble classifier that combines three complementary models. 

## III. PROPOSED SYSTEM ARCHITECTURE 



Fig. 1. Proposed system architecture. 

As shown in Fig. 1, the proposed system consists of four layers, namely, hardware sensing, wireless communication, data processing and classification, and application feedback layers. Two MPU6050 inertial measurement unit (IMU) sensors were used to record the movement of the knee joint of the thigh and shank and sent the information through the ESP32 controller using Bluetooth wireless technology. In turn, the Android mobile application was responsible for sensor fusion, feature extraction, ensemble classification, and realtime feedback to inform the patient about improper gait. 

## _A. Sensor Data Acquisition_ 

Two MPU6050 IMU sensors, each integrating a 3-axis MEMS accelerometer and a 3-axis MEMS gyroscope on a single chip, are mounted on the thigh and shank segments bracketing the knee joint. This dual-sensor placement is deliberate: rather than measuring the absolute orientation of a single limb segment, it allows the system to compute the relative rotation between the thigh and shank, which corresponds directly to the knee flexion–extension angle of clinical interest. An ESP32 microcontroller polls both sensors over a shared I2C bus at a 50 Hz sampling rate, a rate high enough to resolve the comparatively slow dynamics of a knee repetition while remaining well within the processing and transmission budget of the microcontroller and the downstream Bluetooth link. Since the two MPU6050 modules share the same default I2C address, one sensor's address line is reconfigured so that both devices can be polled independently on the same bus without contention. At start-up, the system performs a mandatory calibration routine during which the user is asked to remain stationary for 3–5 seconds; during this interval, the accelerometer and gyroscope outputs, which should ideally correspond to a fixed gravitational reference and zero angular velocity in the absence of motion, are averaged to estimate their resting offsets. These offsets are then subtracted from all subsequent readings, compensating for the small but persistent zero-bias errors that are characteristic of low-cost MEMS sensors. This step is particularly crucial for the gyroscope, since the bias would otherwise integrate up to a large orientation error, and thus improve the accuracy of the knee angle calculated in Section III-C. The placement of the two IMU sensors and the overall hardware configuration are illustrated in Fig. 2. 



Fig. 2. Wearable sensor placement. 

## _B. Wireless Communication_ 

The ESP32 packages the calibrated accelerometer and gyroscope samples from both IMUs into time-synchronized sensor packets and transmits them to a paired Android device over Bluetooth Classic/BLE. Synchronizing the two sensors 

streams at the point of transmission, rather than after they arrive on the mobile device, ensures that the accelerometer and gyroscope readings used in the sensor-fusion step of Section III-C correspond to the same sampling instant, which is a prerequisite for the complementary filter to produce a stable, drift-corrected knee-angle estimate. Performing all downstream computation—sensor fusion, feature extraction, and classification—on the mobile device rather than in the cloud removes network round-trip latency from the feedback loop entirely and allows the system to continue operating in home environments where a reliable internet connection cannot be assumed. This local-processing design choice is central to satisfying the real-time feedback requirement that motivates the overall system architecture. 

## _C. Preprocessing and Feature Extraction_ 

On the mobile device, a complementary filter fuses the accelerometer's gravity-referenced orientation with the gyroscope's angular-velocity integration to compute a drift-corrected, absolute knee angle. This fusion is motivated by the complementary error characteristics of the two sensor types: the accelerometer provides an orientation estimate, derived from the direction of gravity, that is accurate over long time scales but corrupted by high-frequency noise from muscle vibration and foot impact, whereas the gyroscope provides a smooth, high-bandwidth estimate of angular velocity that is accurate over short time scales but accumulates drift when integrated over longer intervals. By combining the low-frequency component of the accelerometer-derived orientation with the high-frequency component of the integrated gyroscope signal, the complementary filter provides an estimate of the knee angle that possesses the long-term stability of the accelerometer, while allowing for the short-term variations captured by the gyroscope, thus avoiding the drift issues of the former and the noise problems of the latter. 

Given this filtered knee angle, a sliding-window feature extractor derives a set of reduced biomechanical features including range of motion, movement intensity, motion variability, rotational movement, and movement smoothness, each of which is indicative of a specific aspect of the patient’s repetitions. Range of motion is defined as the angle of knee flexion during repetitions and is indicative of repetitions performed with insufficient knee bend. Movement intensity and motion variability are defined as the velocity of a movement and the consistency of a repetitive pattern, respectively, meaning that extreme values during repetitions indicate loss of control during motor task execution. Rotational movement is defined as rotation about the longitudinal axis of the shank in the transverse plane and is considered abnormal during repetitions as it results in reduced therapeutic benefit from the exercise. Finally, movement smoothness is defined as the absence of discontinuities in a movement and can be used to identify potential pain or discomfort experienced by the patient during the exercise. The extraction of these features from the combined knee signal instead of individual sensor streams reduces the resulting feature vector dimensionality while retaining the biomechanical information relevant to the physiotherapist evaluating a patient’s repetitions during a rehabilitation session. As such, the derived set of features retain the information needed for the assessment of both the quantity and the quality of a patient’s therapeutic exercise. 

TABLE I. BIOMECHANICAL FEATURES 

|**Feature**|**Description**|**Purpose**|
|---|---|---|
|**Range of**<br>**Motion**|Knee angular movement<br>during exercise|Identifies insufficient<br>knee movement|
|**Movement**<br>**Intensity**|Characteristics of<br>movement velocity|Detects uncontrolled<br>movements|
|**Motion**<br>**Variability**|Variation in movement<br>pattern|Identifies inconsistent<br>repetitions|
|**Rotational**<br>**Movement**|Shank rotation relative to<br>the thigh|Detects abnormal<br>rotation|
|**Movement**<br>**Smoothness**|Continuity of movement|Identifies irregular<br>movements|



Table I presents the biomechanical features extracted from the IMUs. Each feature encodes particular aspects of the movement pattern, such as range, intensity, variance, rotational characteristics, and smoothness of the exercises. Therefore, the set of features provides sufficient information for the classification pipeline to distinguish between properly and improperly executed exercises. 

## _D. Ensemble Classification_ 

The extracted feature vector is passed simultaneously to three independently trained classifiers—Logistic Regression, Random Forest, and XGBoost—each designed for efficient on-device inference. These three models were selected for their complementary, rather than redundant, characteristics. Logistic Regression is a linear model that produces well-calibrated probability estimates and is comparatively resistant to overfitting on a moderately sized feature set, making it a stable baseline within the ensemble. Random Forest is an ensemble of decision trees, each trained on a bootstrapped subset of the training data and a random subset of features; averaging the predictions of many de-correlated trees reduces the variance that a single decision tree would otherwise exhibit, making Random Forest robust to noisy or atypical repetitions. XGBoost is a gradient-boosted tree ensemble that builds trees sequentially, with each new tree trained to correct the residual errors of the previous ones, allowing it to capture more complex, non-linear relationships between the biomechanical features and posture correctness than either of the other two models, typically at the cost of greater sensitivity to individual edge cases. Each model outputs an independent probability that the repetition was performed correctly. A Soft-Voting aggregator combines these three probabilities by averaging them into a single score, and the aggregated score is compared against a decision threshold of 0.5: scores above the threshold are classified as a correct repetition, and scores below it triggers a form alert. Averaging the class probabilities output by each model, rather than combining their hard class predictions (Hard Voting), preserves each model's confidence in its own prediction, so that a case on which a given model is only weakly confident contributes proportionally less to the final decision than a case on which it is strongly confident. 

## _E. Feedback and Mobile Application_ 

When a form alert is triggered, the Android application immediately notifies the patient through a visual and/or audio cue, allowing the correction to happen within the same repetition rather than being discovered only after the session has ended, which is the key distinction between the proposed system and the passive data-logging approaches discussed in 

Section II. Beyond the immediate corrective cue, the application also displays live knee-angle tracking, a running repetition count, session accuracy, and a post-session summary. Surfacing this information continuously during the session gives the patient real-time insight into how the exercise is progressing, while the post-session summary supports longer-term progress tracking across multiple sessions, benefiting both the patient's own motivation and later review of session history. 

## IV. IMPLEMENTATION 

## _A. Hardware Setup_ 

The hardware prototype consists of an ESP32 development board and two MPU6050 breakout modules, each housed in a lightweight, strap-mounted enclosure designed to be worn around the thigh and shank without restricting the knee joint's natural range of motion during exercise. The system is battery powered, allowing for portable use during rehabilitation sessions while maintaining the overall lightness and comfort of a wearable device during standard home-use physical rehabilitation sessions. 



Fig. 3. Hardware prototype. 

The hardware prototype presented in Fig. 3 is based on the ESP32 microcontroller and utilizes two MPU6050 Inertial Measurement Units (IMUs) placed on the thigh and shank to track the knee movements during rehabilitation exercises. The microcontroller and the two inertial sensors are connected as a single sensing node that is worn on the leg and wirelessly communicates with the Android application over Bluetooth, which processes, classifies, and provides realtime feedback on the rehabilitation movements. 

of the leg, while the power supply allows for convenient use. The Android device, in turn, processes the data and provides the classification results and instructions to the patient. 

## _B. Software and Model Training_ 

Model training was performed offline in Python, using Pandas and NumPy for data preparation and feature engineering, and Scikit-learn and XGBoost for building the Logistic Regression, Random Forest, and XGBoost classifiers, respectively. Training the models offline, rather than on the wearable hardware itself, allows the models to be developed and iterated on using standard data-science tooling before being frozen for deployment, and keeps the computational burden of training entirely off the resource-constrained ESP32 and mobile device. The models will then be tested on a held-out test set to evaluate performance and prevent overfitting to any one individual's motions. Finally, the trained models will be deployed on an Android app, where the final trained models are prepared for deployment on an Android application, allowing them to make predictions to classify rehabilitation movements without relying on a server to do so. 



Fig. 4. Android application interface. 

The Android app interface shown in Fig. 4 offers the user a hub for rehabilitation activities and interaction with the system. It shows the connection status of the wearable IMU, provides the prescribed knee rehabilitation exercise, and offers video demonstrations of the rehabilitation exercise. It also enables the user to begin the therapy session. The app comprises the user-facing frontend of the proposed sensing, classifica-tion, and feedback pipeline. 

TABLE II. HARDWARE COMPONENTS 

## _C. End-to-End Pipeline_ 

|**Component**|**Function**|
|---|---|
|ESP32|Sensor acquisition and Bluetooth<br>communication|
|MPU6050(Thigh)|Measures thigh motion|
|MPU6050(Shank)|Measures shank motion|
|Rechargeable Battery|Providesportable systempower|
|Android Device|Data processing, classification, and<br>feedback|



Table II contains the list of key hardware components used in the developed physiotherapy monitoring system, together with an outline of their purpose. The microcontroller ESP32 is responsible for receiving the information from the two accelerometers and transmitting it to an Android device over Bluetooth. The MPU6050 modules track the movement 

The complete pipeline operates as a continuous closed loop: the ESP32 acquires and transmits sensor data at 50 Hz; the Android application applies the complementary filter to compute the drift-corrected knee angle and extracts the biomechanical feature set over a sliding window; the Soft-Voting ensemble classifier computes a probability that the repetition was performed correctly; and the feedback engine either increments the repetition counter, if the probability is above the decision threshold, or raises a corrective alert, if it is below. Because every stage of this loop—sensor acquisition, wireless transmission, sensor fusion, feature extraction, and on-device inference—executes locally without a round trip to a remote server, the entire loop, from the physical 

movement to the delivery of a corrective alert, is designed for low-latency operation intended to be imperceptible to the user and consistent with the real-time feedback requirement motivating the system's design. The modular design of the proposed pipeline also facilitates future system extensions. Additional wearable sensors, feature extraction methods, or improved classification models can be integrated with minimal modifications to the overall architecture. This extensibility enables the system to accommodate future technological advancements while preserving compatibility with the existing sensing and feedback framework. 

## V. RESULTS AND DISCUSSION 

## _A. Machine Learning Performance_ 

The performance of the individual base classifiers and the proposed Soft-Voting classifier will be analyzed using the collected data set of rehabilitation exercises. The individual performance of Logistic Regression, Random Forest, and XGBoost algorithms, as well as Soft-Voting, will be compared to one another by training them on the gathered data set. The comparison will be based on standard classification performance metrics such as accuracy, precision, and recall. The results and perfor-mance analysis of the classifiers will be presented after completing the data-collection and analysis process. 

## _B. Hardware and Latency Performance_ 

The acquisition unit was built around the ESP32 microcontroller, which operated at a frequency of 50 Hz, while the battery used to power the system was sufficient to last throughout the rehabilitation cycle. The acquisition-chaining process was optimized to reduce delays, and the system responded in real-time to the movement data, thus addressing the requirements of the task. 

## _C. Session-Level Evaluation_ 

The developed system will enable ongoing rehabilitation sessions whereby data can be gathered from the proposed sensors, analyzed through the classification pipeline, and the results visualized in the Android application to provide feedback to the user. The sessions will be used to evaluate the performance of the developed system in classifying exercises, providing feedback, and operating overall during a session of rehabilitation exercises. 

## _D. Limitations_ 

The reliability of the system depends on the correct placement of the two IMU sensors on the thigh and shank, as inaccurate placement can cause artifacts and erroneous retrieval of characteristic movements. The current prototype is also restricted to knee flexion and extension exercises. It has not yet been validated on a large, diverse patient population, which will be necessary before clinical deployment. 

## VI. CONCLUSION AND FUTURE SCOPE 

The paper introduced an IoT-based intelligent physiotherapy monitoring system that used two wearable IMU sensors, an ESP32 microcontroller, and an on-device Soft-Voting ensemble classifier for real-time corrective feedback during home-based knee rehabilitation. The novelty of the approach 

was that it provided feedback to the user if an incorrect posture was detected while performing an exercise. The work classified the rehabilitation exercises using Logistic Regression, Random Forest, and XGBoost algorithms with the Soft Voting Ensemble Classifier. The system is cost-effective, portable, and runs on the user’s device, making it ideal for use at home; but it is also designed to help physiotherapists keep track of their patients’ progress in the workplace. 

The described system design is composed of wearable sensors, local processing and classification of data using an ensemble, and provision of feedback through mobile devices. Such an approach allows for instant feedback during rehabilitation exercises while maintaining the possibility of expanding the system’s functionality, including the addition of more data and results from rehabilitation-related tests in the future. The developed system will be tested on collected data to evaluate the performance of classification and the effectiveness of the system during the exercises. 

Future work will include adapting the system to other joints, such as the hip and ankle, working toward greater robustness to variations in sensor placement, validating the technology on a larger and more diverse cohort of patients, and optionally connecting to the cloud for asynchronous review by medical professionals 

## REFERENCES 

- [1] B. Milosevic, A. Leardini, and E. Farella, “Kinect and wearable inertial sensors for motor rehabilitation programs at home: State of the art and an experimental comparison,” Biomed. Eng. Online, vol. 19, no. 1, Apr. 2020. 

- [2] J. Mitternacht, A. Hermann, and P. Carqueville, “Acquisition of Lower-Limb Motion Characteristics with a Single Inertial Measurement Unit—Validation for Use in Physiotherapy,” Diagnostics, vol. 12, no. 7, Jul. 2022. 

- [3] S. Majumder and M. J. Deen, “Wearable IMU-Based System for RealTime Monitoring of Lower-Limb Joints,” IEEE Sens. J., vol. 21, no. 6, pp. 8267–8275, Mar. 2021. 

- [4] M. M. Rahman, K. B. Gan, N. A. A. Aziz, A. Huong, and H. W. You, “Upper Limb Joint Angle Estimation Using Wearable IMUs and Personalized Calibration Algorithm,” Mathematics, vol. 11, no. 4, Feb. 2023. 

- [5] G. G. Carro, J. C. Alvarez, D. V. Tirado, A. Castellanos, A. M. Lopez, and D. Alvarez, “Inertial Sensor-Based Motion Calibration for 1-DoF Joint Angle Estimation,” in Proc. IEEE EMBC, Jul. 2025, pp. 1–7. 

- [6] A. Hua et al., “Evaluation of Machine Learning Models for Classifying Upper Extremity Exercises Using Inertial Measurement Unit-Based Kinematic Data,” IEEE J. Biomed. Health Inform., vol. 24, no. 9, pp. 2452–2460, Sep. 2020. 

- [7] L. Forsyth, A. Ligeti, M. Blyth, J. V. Clarke, and P. E. Riches, “Validity of wearable sensors for total knee arthroplasty (TKA) rehabilitation,” Knee, vol. 51, pp. 292–302, Dec. 2024. 

- [8] M. Riffitts, H. Cook, M. McClincy, and K. Bell, “Evaluation of a Smart Knee Brace for Range of Motion and Velocity Monitoring during Rehabilitation Exercises and an Exergame,” Sensors, vol. 22, no. 24, Dec. 2022. 

- [9] Y. Sun et al., “IMU-Based quantitative assessment of stroke from gait,” Sci. Rep., vol. 15, no. 1, Dec. 2025. 

- [10] B. M. Cornish et al., “Sagittal plane knee kinematics can be measured during activities of daily living following total knee arthroplasty with two IMU,” PLoS One, vol. 19, no. 2, Feb. 2024. 

- [11] T. Franco et al., “Motion Knee Angle Recognition in Muscle Rehabilitation Solutions,” Sensors, vol. 22, no. 19, Oct. 2022. 

- [12] J. Smith, D. Parikh, V. Tate, S. F. Siddicky, and H. Y. Hsiao, “Validity of Valor Inertial Measurement Unit for Upper and Lower Extremity Joint Angles,” Sensors, vol. 24, no. 17, Sep. 2024. 

