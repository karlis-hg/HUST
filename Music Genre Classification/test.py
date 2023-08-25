from classifier import classifier

path = "Test file/jazz.00004.wav"
k = 7
predictions, votes = classifier(path, k)
print("According to my predictions: ")
for i in range(len(predictions)):
    possibility = votes[i] / k * 100
    print(f"There's{possibility: .2f}% chance that it's " + predictions[i].upper())
