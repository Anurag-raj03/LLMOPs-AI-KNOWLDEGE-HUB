ai-knowledgehub/
│
├── infra/                                               # ⚙️ Infrastructure-as-Code (Terraform + K8s + Airflow)
│   ├── terraform/
│   │   ├── main.tf                                     # Root Terraform config (module wiring)
│   │   ├── variables.tf                                # Input variables (AWS_REGION, etc.)
│   │   ├── outputs.tf                                  # Terraform output references
│   │   ├── providers.tf                                # AWS provider definition
│   │   ├── vpc.tf                                      # Networking setup (VPC, subnets)
│   │   ├── eks.tf                                      # EKS cluster creation
│   │   ├── iam.tf                                      # Roles + service accounts (Agents, Airflow)
│   │   ├── s3.tf                                       # S3 buckets for datasets, DVC, model artifacts
│   │   ├── ecr.tf                                      # Container registry
│   │   ├── redis.tf                                    # Elasticache for LangGraph cache
│   │   ├── dynamodb.tf                                 # Feedback storage + human review queue
│   │   ├── prometheus_grafana.tf                       # Monitoring stack (Grafana, Prometheus)
│   │   ├── sqs.tf                                      # Task queues for agent workflows
│   │   ├── secrets_manager.tf                          # Store Gmail OAuth, LangSmith API, etc.
│   │   ├── route53.tf                                  # DNS + SSL (optional)
│   │   └── airflow.tf                                  # Deploy Airflow Helm chart on EKS
│   │
│   └── k8s/                                            # Kubernetes manifests
│       ├── deployment-api.yaml                         # API service deployment
│       ├── service-api.yaml                            # API service configuration
│       ├── retriever-worker.yaml                       # Retriever agent worker
│       ├── agent-worker.yaml                           # Generic worker (for all agents)
│       ├── lora-trainer-job.yaml                       # LoRA fine-tuning job template
│       ├── redis-statefulset.yaml                      # Redis cache for embeddings + LangGraph
│       ├── cronjob-retrain.yaml                        # Periodic retraining trigger
│       ├── prometheus-deployment.yaml
│       ├── grafana-deployment.yaml
│       ├── configmap-secrets.yaml
│       └── airflow/                                    # Airflow setup manifests
│           ├── airflow-deployment.yaml
│           ├── airflow-scheduler.yaml
│           ├── airflow-webserver.yaml
│           └── airflow-configmap.yaml
│
├── orchestrator/                                       # 🌀 Airflow DAGs + Plugins (workflow orchestration)
│   ├── dags/
│   │   ├── ingestion_dag.py                            # Automates ingestion pipeline (calls DVC or custom script)
│   │   ├── retraining_dag.py                           # Triggers LoRA retraining when new feedback arrives
│   │   ├── feedback_loop_dag.py                        # Manages human feedback loop and review queue
│   │   ├── email_agent_dag.py                          # Gmail read/write/send orchestration DAG
│   │   ├── observability_dag.py                        # Collects and pushes system metrics
│   │   └── parallel_agent_dag.py                       # Launch multiple agents concurrently (LangGraph)
│   │
│   ├── plugins/
│   │   ├── dvc_operator.py                             # Custom operator to run DVC stages inside Airflow
│   │   ├── langsmith_plugin.py                         # Auto-log Airflow tasks to LangSmith
│   │   └── email_operator.py                           # Operator for Gmail automation tasks
│   │
│   ├── airflow_config/                                 # Airflow-specific configs
│   │   ├── connections.yaml                            # AWS, Gmail, LangSmith credentials
│   │   ├── variables.yaml                              # DAG configs (frequency, limits)
│   │   └── secrets_backend.yaml                        # Maps to AWS Secrets Manager
│   │
│   └── requirements.txt                                # Apache Airflow + AWS + Kubernetes providers
│
├── data/                                               # 📂 Data management (DVC-tracked)
│   ├── raw/
│   │   ├── arxiv-metadata-oai-snapshot.json
│   │   └── arxiv_subset.csv
│   ├── processed/
│   │   ├── cleaned_docs.jsonl
│   │   ├── processed_chunks.jsonl
│   │   ├── enriched_chunks.jsonl
│   │   └── embeddings_manifest.json
│   ├── embeddings/
│   │   ├── arxiv_index.faiss
│   │   ├── embeddings.npy
│   │   └── metadata.pkl
│   ├── train.jsonl
│   ├── val.jsonl
│   └── feedback_data/
│       ├── retrain_examples.jsonl
│       ├── review_logs.jsonl                           # Human review decisions
│       └── logs/
│
├── dvc.yaml                                            # DVC pipeline for ingestion → training → eval
├── params.yaml                                         # DVC stage hyperparameters
│
├── src/
│   ├── agents/                                         # 🧠 Agentic workers
│   │   ├── base_agent.py                               # Agent base class (plan → act → observe)
│   │   ├── ingestion_agent.py                          # Runs ingestion pipeline on data changes
│   │   ├── retriever_agent.py                          # Builds BM25 + FAISS indexes
│   │   ├── reasoning_agent.py                          # LangGraph reasoning & generation node
│   │   ├── email_agent.py                              # Reads/writes Gmail + triage tasks
│   │   ├── monitor_agent.py                            # Collects metrics, pushes to Prometheus
│   │   ├── human_review_agent.py                       # Manages human-in-the-loop review tasks
│   │   ├── agent_utils.py                              # Retry, async, queue helpers
│   │   └── agent_config.yaml                           # Configs (parallelism, SQS queues, LangSmith endpoints)
│   │
│   ├── ingestion/
│   │   ├── load_docs.py                                # Load arxiv_subset.csv
│   │   ├── preprocess.py                               # Clean text
│   │   ├── chunker.py                                  # Chunk text for embedding
│   │   ├── embed_docs.py                               # Generate FAISS embeddings
│   │   └── metadata_extractor.py                       # Extract tags & keywords
│   │
│   ├── retriever/
│   │   ├── bm25_index.py
│   │   ├── vector_index.py
│   │   ├── reranker.py
│   │   ├── hybrid_retriever.py
│   │   └── retriever_utils.py
│   │
│   ├── rag_graph/                                      # LangGraph-based reasoning + agents graph
│   │   ├── graph_builder.py                            # Build LangGraph nodes
│   │   ├── config_graph.yaml
│   │   ├── run_pipeline.py                             # Run multi-agent reasoning graph
│   │   └── nodes/
│   │       ├── retriever_node.py
│   │       ├── generator_node.py
│   │       ├── summarizer_node.py
│   │       ├── evaluator_node.py
│   │       ├── feedback_node.py
│   │       └── email_node.py                           # Email summarization agent node
│   │
│   ├── training/
│   │   ├── train_lora.py
│   │   ├── eval_lora.py
│   │   ├── dataset_prep.py
│   │   ├── tokenizer_config.json
│   │   ├── model_card.md
│   │   └── lora_config.json
│   │
│   ├── evaluation/
│   │   ├── eval_metrics.py
│   │   ├── auto_grader.py
│   │   ├── langsmith_logger.py
│   │   ├── factuality_eval.py
│   │   ├── relevance_eval.py
│   │   ├── latency_tracker.py
│   │   └── human_eval_collector.py                      # Aggregates human reviews for scoring
│   │
│   ├── api/
│   │   ├── app.py
│   │   ├── dependencies.py
│   │   ├── redis_cache.py
│   │   ├── models.py
│   │   ├── routes/
│   │   │   ├── query.py
│   │   │   ├── feedback.py
│   │   │   ├── monitor.py
│   │   │   ├── agents.py
│   │   │   ├── human_review.py
│   │   │   └── gmail.py                                 # Gmail webhook endpoint (new emails trigger EmailAgent)
│   │   └── middleware/
│   │       ├── telemetry.py
│   │       └── auth.py
│   │
│   ├── feedback/
│   │   ├── feedback_ingest.py
│   │   ├── curator.py
│   │   ├── trigger_retrain.py
│   │   └── human_feedback_mapper.py                     # Maps human feedback → retraining samples
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── s3_utils.py
│   │   ├── config_loader.py
│   │   ├── constants.py
│   │   ├── validation.py
│   │   ├── parallel_utils.py
│   │   └── email_parser.py                              # Gmail message parsing utility
│   │
│   └── services/
│       ├── redis_service.py
│       ├── dynamodb_service.py
│       ├── s3_service.py
│       ├── langsmith_service.py
│       ├── prometheus_service.py
│       ├── gmail_service.py                             # Gmail API (read, send, label)
│       ├── sqs_service.py                               # SQS polling + message dispatch
│       └── airflow_trigger_service.py                   # Trigger DAGs programmatically from API
│
├── ui/                                                  # 🎨 Streamlit Dashboard
│   ├── Home.py
│   ├── pages/
│   │   ├── 1_Query_Assistant.py
│   │   ├── 2_Data_Monitor.py
│   │   ├── 3_Model_Evaluation.py
│   │   ├── 4_Feedback_Insights.py
│   │   ├── 5_System_Status.py
│   │   └── 6_Human_Review.py
│   ├── components/
│   │   ├── chat_box.py
│   │   ├── metrics_cards.py
│   │   ├── feedback_display.py
│   │   ├── chart_widgets.py
│   │   ├── review_panel.py
│   │   └── email_viewer.py                              # Shows incoming emails + summary from EmailAgent
│   ├── assets/
│   │   ├── logo.png
│   │   ├── favicon.ico
│   │   └── styles.css
│   └── utils/
│       ├── api_client.py
│       ├── ui_state.py
│       ├── chart_helpers.py
│       ├── config.py
│       └── review_api.py                               # For human review actions
│
├── models/
│   ├── base_model/
│   ├── tokenizer/
│   └── lora_adapter/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_rag_pipeline_demo.ipynb
│   ├── 03_langgraph_debug.ipynb
│   ├── 04_lora_finetune_results.ipynb
│   └── 05_dashboard_evaluation.ipynb
│
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.trainer
│   ├── Dockerfile.agent
│   ├── Dockerfile.airflow                              # Airflow container image
│   ├── Dockerfile.ui
│   ├── docker-compose.yaml
│   └── .dockerignore
│
├── .github/
│   └── workflows/
│       ├── ci-cd.yaml
│       ├── dvc-retrain.yaml
│       ├── terraform-deploy.yaml
│       ├── airflow-sync.yaml                           # Sync DAGs to Airflow automatically
│       └── notify-slack.yaml
│
├── tests/
│   ├── test_retriever.py
│   ├── test_graph.py
│   ├── test_api.py
│   ├── test_trainer.py
│   ├── test_feedback_loop.py
│   ├── test_ui_api_integration.py
│   ├── test_agents.py
│   ├── test_airflow_dags.py                            # Validate DAG imports and scheduling
│   └── test_gmail_service.py                           # Validate Gmail read/write/send
│
├── scripts/
│   ├── bootstrap_env.sh
│   ├── clean_artifacts.sh
│   ├── export_metrics.py
│   ├── trigger_pipeline.py
│   ├── airflow_dag_uploader.py                         # Push DAGs to Airflow S3/Git-sync
│   └── gmail_token_setup.py                            # Setup and refresh Gmail OAuth token
│
├── requirements.txt
├── requirements-ui.txt
├── requirements-airflow.txt                            # Airflow dependencies
├── setup.cfg
├── README.md
└── LICENSE
