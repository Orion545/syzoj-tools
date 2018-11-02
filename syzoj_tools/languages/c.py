#!/usr/bin/python3
import os
import tempfile
import subprocess
import shutil

class ProblemCLanguage:
    def __init__(self, problem, config):
        self.problem = problem
        self.config = config

    def judge_session(self, source):
        return ProblemCLanguageJudgeSession(self, source)

class ProblemCLanguageJudgeSession:
    def __init__(self, language, source):
        self.language = language
        self.source = source

    def pre_judge(self):
        print("Compiling c file %s" % self.source)
        self.tempdir = tempfile.mkdtemp()
        self.prog = os.path.join(self.tempdir, "prog")
        try:
            subprocess.run(["gcc", self.source, "-o", self.prog], check=True)
        except subprocess.CalledProcessError:
            print("Compilation failed")
            return "Compilation Error"

    def run_judge(self, case):
        workdir = tempfile.mkdtemp()
        if not "input-file" in case.config:
            stdin = open(case.input_data, "rb")
        else:
            shutil.copyfile(case.config["input-data"], os.path.join(workdir, case.config["input-file"]))
            stdin = subprocess.DEVNULL

        if not "output-file" in case.config:
            stdout = tempfile.NamedTemporaryFile()
        else:
            outfile = os.path.join(workdir, case.config["output-file"])
            stdout = subprocess.DEVNULL
        
        try:
            subprocess.run([self.prog], stdin=stdin, stdout=stdout, cwd=workdir, check=True)
        except subprocess.CalledProcessError:
            return (False, "Runtime error")
        
        if not "output-file" in case.config:
            return (True, stdout.name)
        else:
            if not os.path.isfile(outfile):
                return (False, "No output")
            else:
                return (True, outfile)
    
    def post_judge(self):
        shutil.rmtree(self.tempdir)
