"""
Command-line interface for ZKvsAI
"""

import click
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from . import PrivateRAG, NockchainVerifier

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """
    ZKvsAI - Privacy-Preserving AI/RAG Platform

    Brings AI to your data, not your data to AI.
    """
    pass


@main.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--model", default="sentence-transformers/all-MiniLM-L6-v2", help="Embedding model")
def index(directory, model):
    """Index documents from a directory"""
    console.print(f"[bold blue]Indexing documents from: {directory}[/bold blue]")

    rag = PrivateRAG(documents_dir=directory, model_name=model)

    stats = rag.get_stats()

    console.print(f"[green]✓[/green] Indexed {stats['num_documents']} documents")
    console.print(f"[green]✓[/green] Created {stats['num_chunks']} chunks")
    console.print(f"[green]✓[/green] Commitment: {stats['commitment'][:16]}...")


@main.command()
@click.argument("directory", type=click.Path(exists=True))
@click.argument("question")
@click.option("--top-k", default=3, help="Number of results to retrieve")
@click.option("--proof/--no-proof", default=False, help="Generate ZK proof")
@click.option("--verify/--no-verify", default=False, help="Verify proof on Nockchain")
def query(directory, question, top_k, proof, verify):
    """Query your private documents"""
    console.print(f"[bold blue]Query: {question}[/bold blue]\n")

    # Initialize RAG
    rag = PrivateRAG(documents_dir=directory)

    # Execute query
    with console.status("[bold green]Searching documents..."):
        response = rag.query(question, top_k=top_k, generate_proof=proof)

    # Display answer
    console.print("[bold]Answer:[/bold]")
    console.print(response.answer)
    console.print()

    # Display sources
    console.print("[bold]Sources:[/bold]")
    for i, chunk in enumerate(response.sources, 1):
        console.print(f"[cyan]{i}.[/cyan] Doc {chunk.doc_id} (chunk {chunk.chunk_id})")

    # Display proof if generated
    if proof and response.proof:
        console.print(f"\n[bold]Proof:[/bold] {response.proof[:32]}...")

        # Verify if requested
        if verify:
            console.print("\n[bold yellow]Verifying proof on Nockchain...[/bold yellow]")
            verifier = NockchainVerifier()

            stats = rag.get_stats()
            result = verifier.verify_query(
                proof=response.proof,
                document_commitment=stats['commitment'],
                model_hash=stats['model_hash'],
                timestamp=int(response.timestamp)
            )

            if result.is_valid:
                console.print("[bold green]✓ Proof verified successfully![/bold green]")
            else:
                console.print(f"[bold red]✗ Verification failed: {result.message}[/bold red]")


@main.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--output", "-o", default="commitment.json", help="Output file")
def register(directory, output):
    """Register document commitment on Nockchain"""
    console.print(f"[bold blue]Registering documents from: {directory}[/bold blue]")

    # Initialize RAG
    rag = PrivateRAG(documents_dir=directory)

    # Generate commitment
    commitment = rag.register_documents()
    rag.export_commitment(output)

    console.print(f"[green]✓[/green] Commitment: {commitment}")
    console.print(f"[green]✓[/green] Saved to: {output}")

    # Register on Nockchain
    console.print("\n[bold yellow]Registering on Nockchain...[/bold yellow]")
    verifier = NockchainVerifier()

    if not verifier.health_check():
        console.print("[red]✗ Nockchain verifier not available[/red]")
        console.print("  Start the verifier with: cd nockapp && nockup project run")
        return

    result = verifier.register_commitment(commitment)

    if result.get("success"):
        console.print("[bold green]✓ Registered successfully![/bold green]")
        if "id" in result:
            console.print(f"  Registration ID: {result['id']}")
    else:
        console.print(f"[red]✗ Registration failed: {result.get('error')}[/red]")


@main.command()
@click.argument("directory", type=click.Path(exists=True))
def stats(directory):
    """Show statistics about indexed documents"""
    rag = PrivateRAG(documents_dir=directory)
    stats_data = rag.get_stats()

    table = Table(title="RAG Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Documents", str(stats_data['num_documents']))
    table.add_row("Chunks", str(stats_data['num_chunks']))
    table.add_row("Embedding Dimension", str(stats_data['embedding_dimension']))
    table.add_row("Model", stats_data['model_name'])
    table.add_row("Model Hash", stats_data['model_hash'][:16] + "...")
    table.add_row("Commitment", stats_data['commitment'][:16] + "...")

    console.print(table)


@main.command()
def info():
    """Show ZKvsAI system information"""
    rprint("[bold]ZKvsAI - Privacy-Preserving AI/RAG Platform[/bold]")
    rprint("\n[cyan]Architecture:[/cyan]")
    rprint("  • Local RAG: Documents never leave your device")
    rprint("  • ZK Proofs: Verify computation without revealing data")
    rprint("  • Nockchain: Decentralized verification")

    rprint("\n[cyan]Features:[/cyan]")
    rprint("  ✓ Private document indexing")
    rprint("  ✓ Local embedding generation")
    rprint("  ✓ Local semantic search")
    rprint("  ✓ Zero-knowledge proof generation")
    rprint("  ✓ On-chain verification")

    rprint("\n[cyan]Commands:[/cyan]")
    rprint("  zkrag index <dir>        Index documents")
    rprint("  zkrag query <dir> <q>    Query documents")
    rprint("  zkrag register <dir>     Register on Nockchain")
    rprint("  zkrag stats <dir>        Show statistics")


if __name__ == "__main__":
    main()
