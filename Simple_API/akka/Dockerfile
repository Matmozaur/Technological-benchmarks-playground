# Use a base image with a JVM and Scala pre-installed
FROM hseeberger/scala-sbt:8u242_1.4.1_2.13.3

# Set the working directory in the container
WORKDIR /app

# Copy the Scala source code and build.sbt file to the working directory
COPY . /app

# Build the Scala project
RUN sbt compile

# Expose the port on which the server will listen (change it if needed)
EXPOSE 8080

# Start the Scala application
CMD sbt run
