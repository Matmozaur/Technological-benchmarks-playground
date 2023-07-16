# Use a base image with Java JDK
#FROM openjdk:11-jdk-slim

FROM hseeberger/scala-sbt:11.0.12_1.5.5_2.13.6

# Set the working directory inside the container
WORKDIR /app

# Install Scala
RUN apt-get update && apt-get install -y scala

COPY app/build.sbt /app

# Trigger the sbt dependency download (caches dependencies)
RUN sbt update

# Copy the Scala source code
COPY app/Main.scala /app

EXPOSE 8085

# Compile and run the Scala application
CMD ["sbt", "run"]

# Compile and run the Scala application
#CMD ["scala", "-nocompdaemon", "Main.scala"]