from tensorflow.keras.models import load_model

model = load_model("./best_model.keras", compile=False)
model.summary()

print(model.input_shape)
