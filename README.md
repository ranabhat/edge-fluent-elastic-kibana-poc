# Unified Edge Apps Logging Proof of Concept

### Requirement

1. Create network `log-redirect`.
2. Run `docker-compose-elastic-kibana.yaml`, configure `kibana`
	- To generate a new enrollment token, run the following command from the Elasticsearch installation directory: `bin/elasticsearch-create-enrollment-token --scope kibana`
	- Retrive `verification` code from kibana, run the following command from the Kibana `bin/kibana-verification-code`
	- Reset `password` for login as user `elastic`, run the following command from the Elasticsearch `bin/elasticsearch-reset-password -u elastic`

3. Run `docker-compose` that runs `fluent-bit` service and simple python app `exampled` that send log to fluentbit
	- Make sure the `fluent-bit.conf` `[OUTPUT]` section has correct `HTTP_User` and `HTTP_Passwd` 
	- The working `fluent-bit.conf` looks like follwing
	```conf
		[SERVICE]
			Flush           5
			Daemon          off
			Log_Level       debug

		[INPUT]
			Name         tcp
			Listen       0.0.0.0
			Port         24224
			
		[OUTPUT]
			Name es
			Match *
			Host elasticsearch
			Port 9200
			Retry_Limit False
			Logstash_Format On
			HTTP_User elastic
			HTTP_Passwd kO7R+BCAhNdty+JfODZm
			tls On
			tls.verify Off
			Suppress_Type_Name On

	```

4. The prod setup is in `docker-compose.yaml`

### Resources

1. [Getting Started with Elastic Stack and docker compose](https://www.elastic.co/blog/getting-started-with-the-elastic-stack-and-docker-compose)