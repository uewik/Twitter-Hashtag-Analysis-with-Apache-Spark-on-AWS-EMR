# Twitter Hashtag Analysis with Apache Spark on AWS EMR

A cloud computing project that analyzes Twitter data to identify and rank the most popular hashtags using Apache Spark on Amazon EMR.

## Project Overview

This project processes Twitter JSON data to extract, count, and rank hashtags from various text fields including tweet content, user descriptions, and property texts. The analysis is performed using Apache Spark on AWS EMR cluster for distributed computing scalability.

## Features

- **Distributed Processing**: Utilizes Apache Spark for large-scale data processing
- **Cloud Integration**: Runs on Amazon EMR cluster with S3 storage
- **Hashtag Extraction**: Extracts hashtags from multiple text sources in Twitter data
- **Top-K Analysis**: Identifies and ranks the top 20 most frequent hashtags
- **Scalable Architecture**: Handles both small (`tinyTwitter.json`) and large (`smallTwitter.json`) datasets

## Data Sources

- **Input**: Twitter JSON data stored in S3 bucket (`s3://p2-inputdata/smallTwitter.json`)
- **Output**: Top 20 hashtags with counts saved to S3 (`s3://cloudcomputingvt/Hao/output`)

## Architecture

```
Twitter JSON Data (S3) → EMR Cluster (Spark) → Processed Results (S3)
```

## Data Processing Pipeline

1. **Data Ingestion**: Reads Twitter JSON data from S3
2. **Text Concatenation**: Combines text from multiple fields:
   - `doc.text` (tweet content)
   - `doc.user.description` (user bio)
   - `value.properties.text` (property text)
3. **Word Tokenization**: Splits concatenated text into individual words
4. **Hashtag Filtering**: Extracts words starting with '#' using regex pattern
5. **Aggregation**: Counts hashtag frequencies
6. **Ranking**: Sorts hashtags by count in descending order
7. **Output**: Exports top 20 hashtags to CSV format in S3

## Technical Stack

- **Language**: Python
- **Big Data Framework**: Apache Spark (PySpark)
- **Cloud Platform**: Amazon Web Services (AWS)
- **Compute Service**: Amazon EMR
- **Storage**: Amazon S3
- **Data Format**: JSON (input), CSV (output)

## File Structure

```
.
├── final.py          # Main Spark application
├── README.md         # Project documentation
└── tinyTwitter.json  # Sample data file (local testing)
```

## Code Highlights

### Key PySpark Operations Used:
- `concat_ws()`: Concatenates multiple text fields
- `explode()` + `split()`: Tokenizes text into words
- `regexp_extract()`: Extracts hashtags using regex pattern
- `groupBy()` + `count()`: Aggregates hashtag frequencies
- `orderBy()`: Sorts results by count

### Example Output:
The application identifies the top 20 most frequent hashtags from the Twitter dataset, such as:
```
+----------+-----+
|   hashtag|count|
+----------+-----+
|  #example| 1234|
| #trending|  987|
|  #popular|  654|
+----------+-----+
```

## Setup and Deployment

### Prerequisites
- AWS Account with EMR and S3 access
- Twitter JSON dataset uploaded to S3
- EMR cluster configured with Spark

### Running the Application
1. Upload `final.py` to EMR cluster or S3
2. Submit Spark job:
   ```bash
   spark-submit final.py
   ```
3. Monitor execution through EMR console
4. Retrieve results from S3 output location

### Configuration Options
- Modify input path: Update `spark.read.json()` path
- Adjust result count: Change `.limit(20)` to desired number
- Customize output location: Update `output_path` variable

## Performance Considerations

- **Data Locality**: Input and output stored in S3 for optimal EMR integration
- **Resource Optimization**: Uses `coalesce(1)` to minimize output file fragmentation
- **Memory Management**: Spark automatically manages distributed memory allocation
- **Scalability**: Can process datasets of varying sizes (tiny to large)

## Results

The application successfully processes Twitter data and generates insights about hashtag popularity trends, which can be used for:
- Social media trend analysis
- Marketing campaign optimization
- Content strategy development
- Real-time sentiment tracking

## Future Enhancements

- Real-time streaming analysis using Spark Streaming
- Integration with additional social media platforms
- Advanced text preprocessing and cleaning
- Machine learning-based trend prediction
- Interactive dashboard for result visualization

## Author

Developed for Cloud Computing coursework - Project 2

## License

This project is developed for academic purposes as part of a cloud computing course.
