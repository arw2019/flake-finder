# flake-finder
`flake-finder` is a simple Django app to automate optical detection of crystalline films on wafers.

### Problem Outline

Many materials physicists study so-called two-dimensional materials. Crudely speaking, these are atomically thin films of a given material that possess many amazing properties such as unbelievable strength, transparency to light and lossless electrical conduction.

Typical specimens of these materials cannot be seen with the naked eye. Furthermore, the current best way of producing them yields many differently shaped pieces strewn over a relatively large, mostly empty, area. To find the specimen to be used in their device, scientists manually search optical microscope images until they find a candidate. 

`flake-finder` addressed this problem through algorithmically identifying candidate flakes from images, reducing hours of manual searching to just a few clicks.
In the current version of the repo I use a lightweight detection algorithm known as [Otsu's method](https://en.wikipedia.org/wiki/Otsu%27s_method) but more sophisticated algorithms such as Convolutional
Neural Networks ([see paper](https://arxiv.org/abs/1906.11220?)) have also been found to work.

### Requirements and Goals

#### Functional
* Users should be able to upload raw optical images and download/view both raw & labelled images
* Users should be able to search flakes based on attributes such as specimen size
* Users should be able to delete used candidates from the system.
* The system should send email reminders to alert users about insertions/deletions of candidates.

#### Non-functional
* The service should be highly available.
* Consistency should be prioritized over latency. We want to avoid multiple users selecting the same candidate from the archive.
* The system should be highly reliable. Candidate images should never be lost.

### Design

#### Database Schema
A simple implementation would involve two tables, one for Images and one for Users. In the Chip table we would store some 
searchable properties of the candidates within the image and the user who provided the image. In the API users could search candidates 
based on these attributes. 

#### SQL vs NoSQL
A straightforward approach for storing this schema would be to use RDBMS such as `MySQL` or (my choice) `PostgreSQL`. The images themselves need to
be stored in a distributed file services such as `HDFS` or (my choice) `S3`.

An alternative approach would be to use a key value store such as `Cassandra`. That approach would offer more flexibility to users, allowing them to store 
metadata such as image labels obtained with different algorithms and notes on the candidate.

#### Data Sharding
We would want to generate a unique ImageID for every upload and assign an image to its partition based on a hash of its id.

#### Caching
It may be a good idea to cache hot database rows. LRU (least recently used) would be a reasonable cache eviction policy. The idea would be 
to speed up the system for a user who is working with images they recently uploaded or browsed.


## Deploying the app
I found [these instructions](https://www.1strategy.com/blog/2017/05/23/tutorial-django-elastic-beanstalk/)  helpful for deploying the app on AWS. They ought to follow through for this repo. One note: make sure to choose the Python 3.6 Amazon Linux 2 platform (I ran into problems on the Python 3.7 platform which I haven't yet resolved).
