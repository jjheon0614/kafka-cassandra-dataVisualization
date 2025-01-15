 # kafka-cassandra-dataVisualization

This project involves deploying an end-to-end data pipeline using Docker with the following components:

- Kafka: Data streaming
- Cassandra: NoSQL database
- Jupyter Lab: Data analysis and visualization

It will stream weather, faker data, cryptocurrency with following steps. The demonstartion can be seen [here](https://youtu.be/Y3lhjkPVgRQ)

## Steps

1. Create docker networks

```shell
docker network create kafka-network  
docker network create cassandra-network
```


2. Start Cassandra and kafka container
```shell
docker-compose -f cassandra/docker-compose.yml up -d
docker-compose -f kafka/docker-compose.yml up -d

docker ps -a # checking the container is running
```

3. Enter Kafka UI at http://localhost:9000 and add the cluster

# Task 1: Weather

1. start owm producer container
```shell
docker-compose -f owm-producer/docker-compose.yml build
docker-compose -f owm-producer/docker-compose.yml up
```

2. start consumer container
```shell
docker-compose -f consumers/docker-compose.yml build
docker-compose -f consumers/docker-compose.yml up
```

3. Go to Cassandra shell and check the data is loaded
```shell
docker exec -it cassandra bash

cqlsh --cqlversion=3.4.4 127.0.0.1

use kafkapipeline;

select * from weatherreport;
```

# Task 2: faker api

1. Create table in cassandra shell

```shell
CREATE TABLE IF NOT EXISTS  
kafkapipeline.fakerdata (  
	name TEXT,  
	address TEXT,  
	year INT,
	phone_number TEXT,
	job TEXT,
	email TEXT,
	company TEXT,
	city TEXT,
	state TEXT,
	country TEXT,
	PRIMARY KEY (name, address)  
);
```

2. Start faker producer contiainer

```shell
docker-compose -f faker-producer/docker-compose.yml build
docker-compose -f faker-producer/docker-compose.yml up
```

3. it will see the data in the consumer window
4. go to the Cassandra shell and check the data is loaded

```shell
select * from fakerdata;
```

# Task 3: Cryptocurrency

Get the API key from the binance which is streaming the data of the crypto currency. It can give btc, eth, and doge etc.

1. Create table in cassandra shell

```shell
CREATE TABLE IF NOT EXISTS  
kafkapipeline.cryptodata (  
	date TIMESTAMP,
	btc TEXT,  
	eth TEXT,  
	doge TEXT,
	PRIMARY KEY (btc, date)  
);
```

2. Start crypto producer contiainer

```shell
docker-compose -f crypto-producer/docker-compose.yml build
docker-compose -f crypto-producer/docker-compose.yml up
```

3. it will see the data in the consumer window
4. go to the Cassandra shell and check the data is loaded

```shell
select * from cryptodata;
```


## Data visualization

1. Execute data visualization and go to  http://localhost:8888
```shell
docker-compose -f data-vis/docker-compose.yml up -d
```

2. import library and use DF function to get the datas (weather, faker, and cryptocurrency)

# Task 4

Reference for the relevance between weather and cryptocurrency https://www.finder.com/cryptocurrency-weather-report

1. Show the relevance between btc and Seoul weather
```python
# Plotting btc data
fig, ax1 = plt.subplots(figsize=(20, 6))
ax1.plot(btc_table['date'], btc_table['btc'], color='blue')
ax1.set_xlabel("Time")
ax1.set_ylabel("BTC Price", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_title("BTC and Seoul Temperature Data Recorded")

# Creating a second y-axis for temperature
ax2 = ax1.twinx()
ax2.plot(seoul_weather['forecast_timestamp'], seoul_weather['temp'] - 273.15, color='red')
ax2.set_ylabel("Temperature (°C)", color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Setting the number of ticks for temperature y-axis
num_ticks_temp = 5
ax1.yaxis.set_major_locator(plt.MaxNLocator(num_ticks_temp))

plt.show()
```

## Result
When the temperature in Seoul decrease, the price of the btc increase.


2. Show the relevance between eth and Vancouver weather
```python
# Plotting btc data
fig, ax1 = plt.subplots(figsize=(20, 6))
ax1.plot(eth_table['date'], eth_table['eth'], color='blue')
ax1.set_xlabel("Time")
ax1.set_ylabel("ETH Price", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_title("ETH and Vancouver Temperature Data Recorded")

# Creating a second y-axis for temperature
ax2 = ax1.twinx()
ax2.plot(vancouver_weather['forecast_timestamp'], vancouver_weather['temp'] - 273.15, color='red')
ax2.set_ylabel("Temperature (°C)", color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Setting the number of ticks for temperature y-axis
num_ticks_temp = 5
ax1.yaxis.set_major_locator(plt.MaxNLocator(num_ticks_temp))
  

plt.show()
```

## Result
When the temperature in Vancouver decrease, the price of the eth increase.

### To stopped everything
```shell
docker-compose -f data-vis/docker-compose.yml down # stop visualization node  
docker-compose -f consumers/docker-compose.yml down # stop the consumers  
docker-compose -f owm-producer/docker-compose.yml down # stop open weather map producer  
docker-compose -f faker-producer/docker-compose.yml down
docker-compose -f crypto-producer/docker-compose.yml down
docker-compose -f kafka/docker-compose.yml down # stop zookeeper, broker, kafka-manager and kafka-connect services  
docker-compose -f cassandra/docker-compose.yml down # stop Cassandra  
docker network rm kafka-network
docker network rm cassandra-network
```