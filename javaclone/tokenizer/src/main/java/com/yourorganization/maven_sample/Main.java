package com.yourorganization.maven_sample;

import java.io.IOException;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.util.List;

import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.utils.SourceRoot;
import com.github.javaparser.utils.Pair;
import com.github.javaparser.utils.SourceZip;


public class Main {

    public static void parseDir(String dirname) {
        SourceRoot sourceRoot = new SourceRoot(FileSystems.getDefault().getPath(dirname));
        List<ParseResult<CompilationUnit>> results;

        try {
            results = sourceRoot.tryToParse();
        } catch (IOException ioException) {
            ioException.printStackTrace();
            System.exit(1);
            return;
        }
        boolean hasError = false;
        for (ParseResult<CompilationUnit> result: results) {
            hasError |= LogicPositivizer.parse(result, null);
        }
        if (hasError) {
            System.exit(2);
        }
    }

    public static void parseZip(String zipFile) {
        SourceZip sourceZip = new SourceZip(FileSystems.getDefault().getPath(zipFile));
        List<Pair<Path, ParseResult<CompilationUnit>>> results;
        try {
            results = sourceZip.parse();
        } catch (IOException ioException) {
            ioException.printStackTrace();
            System.exit(1);
            return;
        }
        for (Pair<Path, ParseResult<CompilationUnit>> pair : results) {
            LogicPositivizer.parse(pair.b, pair.a.toString());
        }
    }

    public static void main(String[] args) {
        if (args[0].toLowerCase().strip().endsWith(".zip")) {
            parseZip(args[0]);
        } else {
            parseDir(args[0]);
        }
    }

}