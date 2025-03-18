from ..utils import cmd_run

def clustal_omega_run(
        input_fasta, output_fasta, binary_path="clustalo", 
        force:bool=False, threads:int=4) -> None:
    cmd = [binary_path, "-i", input_fasta, "-o", output_fasta, f"--threads={threads}"]
    if force:
        cmd.append("--force")
    cmd_run(cmd)