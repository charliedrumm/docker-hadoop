package diseasymptomanalysis;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.log4j.Logger;

public class SymptomDiseaseAnalysis {
    private static final Logger logger = Logger.getLogger(SymptomDiseaseAnalysis.class);

    public static class SymptomMapper extends Mapper<Object, Text, Text, Text> {
        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            try {
                String[] fields = value.toString().split(",");
                if (fields.length < 6) {
                    return; // Skip if data is incomplete
                }

                String disease = fields[0];
                String symptoms = String.format("Fever:%s Cough:%s Fatigue:%s DifficultyBreathing:%s Age:%s Gender:%s",
                        fields[1], fields[2], fields[3], fields[4], fields[5], fields[6]);

                context.write(new Text(disease), new Text(symptoms));
            } catch (Exception e) {
                System.err.println("Error processing record: " + e.getMessage());
            }
        }
    }

    public static class SymptomReducer extends Reducer<Text, Text, Text, Text> {
        @Override
        public void reduce(Text key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            int feverCount = 0;
            int coughCount = 0;
            int fatigueCount = 0;
            int difficultyBreathingCount = 0;
            int recordCount = 0;

            for (Text val : values) {
                String[] symptoms = val.toString().split(" ");
                for (String symptom : symptoms) {
                    if (symptom.startsWith("Fever:Yes"))
                        feverCount++;
                    if (symptom.startsWith("Cough:Yes"))
                        coughCount++;
                    if (symptom.startsWith("Fatigue:Yes"))
                        fatigueCount++;
                    if (symptom.startsWith("DifficultyBreathing:Yes"))
                        difficultyBreathingCount++;
                }
                recordCount++;
            }

            String output = String.format(
                    "Fever: %d, Cough: %d, Fatigue: %d, Difficulty Breathing: %d, Records Analyzed: %d",
                    feverCount, coughCount, fatigueCount, difficultyBreathingCount, recordCount);
            context.write(key, new Text(output));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length < 2) {
            System.err.println("Usage: symptomdiseaseanalysis <in> [<in>...] <out>");
            System.exit(2);
        }
        Job job = Job.getInstance(conf, "symptom-disease-analysis");
        job.setJarByClass(SymptomDiseaseAnalysis.class);
        job.setMapperClass(SymptomMapper.class);
        job.setReducerClass(SymptomReducer.class);
    
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
    
        for (int i = 0; i < otherArgs.length - 1; ++i) {
            FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
        }
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[otherArgs.length - 1]));
    
        boolean success = job.waitForCompletion(true);
    
        if (success) {
            logger.info("Application is now ready at localhost:3000. Symptom-disease analysis completed successfully using Spark.");
        } else {
            logger.error("Job failed!");
        }
    
        System.exit(success ? 0 : 1);
    }
}    