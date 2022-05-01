%% Load Image Dataset


% inspect the number of images per category, as well as category labels


%% Prepare Training and Validation Image Sets

%% Create a Visual Vocabulary and Train an Image Category Classifier

% Creating Bag-Of-Features.

% Encoding images using Bag-Of-Features.
img = readimage(imds, 1);
featureVector = encode(bag, img);

% Plot the histogram of visual word occurrences
figure
bar(featureVector)
title('Visual word occurrences')
xlabel('Visual word index')
ylabel('Frequency of occurrence')

%% Training an image category classifier for 5 categories.
categoryClassifier = trainImageCategoryClassifier(trainingSet, bag);

%% Evaluate Classifier Performance

% on training set
confMatrix = evaluate(categoryClassifier, trainingSet);

% on validation set
confMatrix_val = evaluate(categoryClassifier, validationSet);

% Compute average accuracy
avg_acc = mean(diag(confMatrix_val));

%% instance study
% read an image
img = imread(fullfile('/Users/ishug/Desktop/hw3/q7_code/q7_image/office_images','backpack','frame_0001.jpg'));
figure
imshow(img)

% run classification
[labelIdx, scores] = predict(categoryClassifier, img);
labelName = categoryClassifier.Labels(labelIdx);
disp(labelName)

