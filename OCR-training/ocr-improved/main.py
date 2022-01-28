import pipeline
if __name__ == "__main__":
    pipeline = pipeline.Pipeline(2,1024)
    predicted_result = pipeline.recognize("med1.jpeg")