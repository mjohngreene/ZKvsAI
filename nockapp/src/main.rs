// ZK-RAG Verifier NockApp - Rust HTTP Driver
//
// Provides HTTP API for proof verification

use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::{IntoResponse, Response},
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::RwLock;
use tower_http::cors::{Any, CorsLayer};
use tracing::info;

// Request/Response Types

#[derive(Debug, Serialize, Deserialize)]
struct RegisterDocumentRequest {
    commitment: String,
    owner: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct RegisterModelRequest {
    model_hash: String,
    model_name: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct VerifyQueryRequest {
    proof: String,
    document_commitment: String,
    model_hash: String,
    timestamp: u64,
}

#[derive(Debug, Serialize, Deserialize)]
struct SuccessResponse {
    success: bool,
    id: Option<u64>,
}

#[derive(Debug, Serialize, Deserialize)]
struct VerificationResponse {
    valid: bool,
    query_id: Option<u64>,
    message: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct ErrorResponse {
    error: String,
}

// Placeholder kernel (until NockApp integration)
type SharedState = Arc<RwLock<MockKernel>>;

struct MockKernel {
    next_id: u64,
}

impl MockKernel {
    fn new() -> Self {
        Self { next_id: 1 }
    }

    fn next_id(&mut self) -> u64 {
        let id = self.next_id;
        self.next_id += 1;
        id
    }
}

// HTTP Handlers

async fn register_document(
    State(kernel): State<SharedState>,
    Json(payload): Json<RegisterDocumentRequest>,
) -> Response {
    info!("Registering document commitment: {}", &payload.commitment[..16]);

    let mut kernel = kernel.write().await;
    let id = kernel.next_id();

    // TODO: Send to Hoon kernel via noun
    // For now, just return success

    (
        StatusCode::CREATED,
        Json(SuccessResponse {
            success: true,
            id: Some(id),
        }),
    )
        .into_response()
}

async fn register_model(
    State(kernel): State<SharedState>,
    Json(payload): Json<RegisterModelRequest>,
) -> Response {
    info!("Registering model: {}", payload.model_name);

    let mut kernel = kernel.write().await;
    let id = kernel.next_id();

    // TODO: Send to Hoon kernel

    (
        StatusCode::CREATED,
        Json(SuccessResponse {
            success: true,
            id: Some(id),
        }),
    )
        .into_response()
}

async fn verify_query(
    State(kernel): State<SharedState>,
    Json(payload): Json<VerifyQueryRequest>,
) -> Response {
    info!("Verifying query proof");

    // TODO: Actual ZK proof verification via Hoon kernel
    // For now, placeholder verification

    let mut kernel = kernel.write().await;
    let id = kernel.next_id();

    // Placeholder - always valid
    let is_valid = true;

    (
        StatusCode::CREATED,
        Json(VerificationResponse {
            valid: is_valid,
            query_id: Some(id),
            message: if is_valid {
                "Proof verified successfully".to_string()
            } else {
                "Proof verification failed".to_string()
            },
        }),
    )
        .into_response()
}

async fn get_query(State(_kernel): State<SharedState>, Path(id): Path<u64>) -> Response {
    info!("Getting query: {}", id);

    // TODO: Query Hoon kernel

    (
        StatusCode::OK,
        Json(serde_json::json!({
            "id": id,
            "verified": true
        })),
    )
        .into_response()
}

async fn health_check() -> &'static str {
    "OK"
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize tracing
    tracing_subscriber::fmt::init();

    // Initialize kernel state
    let kernel = Arc::new(RwLock::new(MockKernel::new()));

    // Configure CORS
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    // Build router
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/api/v1/document/register", post(register_document))
        .route("/api/v1/model/register", post(register_model))
        .route("/api/v1/query/verify", post(verify_query))
        .route("/api/v1/query/:id", get(get_query))
        .layer(cors)
        .with_state(kernel);

    // Start server
    let addr = "0.0.0.0:8080";
    info!("ZK-RAG Verifier starting on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
