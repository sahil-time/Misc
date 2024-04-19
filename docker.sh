# DOCKER ORBIT

# Remove all cached images etc.
# docker system prune -a
docker rmi sahisha2-test-container

# Build Docker Container
docker build -t sahisha2-test-container .

# Run the container
docker run -it --rm sahisha2-test-container
