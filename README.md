## Marketing segmentation task

A repo to house a 3hr marketing segmentation exercise.

This repo is designed to be a reproducible minature data science project that takes data (data/raw) and then follows reproductible steps to achieve the output.

I've set it up the way I would if it were a professional project - just install requirements.txt and you can run the same pipeline and produce the same results.

# A note on timekeeping

The interview/task brief included a time limit of 3 hours. I've taken that very literally and created timekeeping-logs.csv where I record how long each step took me, so that I can demonstrate what I can achieve under time constraints.

# Approach to segmentation

Here I'm taking what I think is quite a conventional approach to segmentation:

1. Audit data, clean, engineer features if required
2. Exploratory analysis
3. Come up with segment hypotheses
4. Use clustering techniques (in this case: kmeans and gaussian mixture modelling) for some unsupervised work
5. Select and profile segments
6. Make recommendations, produce final report

# Method

My approach here is a staged analysis pipeline, working through:

01-data-audit
02-feature-engineering
03-eda
04-clustering
05-segment-profiling
06-recommendations
07-final-report

At the end of each stage of analysis, I evaluate the results and decide what the next stage should incorporate.

# Use of AI tools

To manage this repo and conduct each stage of analysis, I've chosen to work with Codex.

The three hour time limit is very restrictive if I'm to achieve everything I want to within the allowed time, but by imposing a staged structure and pre-planning the techniques used to achieve the objectives of the brief I can get a lot more done than hand-coding.

It's worth pointing out that I can hand-code projects like this: my MSc Disseration included K means clustering, and I worked on that before usable AI coding tools were available.
