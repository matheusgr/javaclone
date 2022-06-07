package com.yourorganization.maven_sample;

import java.io.IOException;
import java.nio.file.FileSystems;
import java.util.List;
import java.util.Optional;

import com.github.javaparser.ParseResult;
import com.github.javaparser.Problem;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.visitor.GenericVisitorWithDefaults;
import com.github.javaparser.utils.SourceRoot;

/**
 * Some code that uses JavaParser.
 */
public class LogicPositivizer {
    public static void main(String[] args) {
        
        SourceRoot sourceRoot = new SourceRoot(FileSystems.getDefault().getPath(args[0]));
        List<ParseResult<CompilationUnit>> results;
        boolean hasError = false;

        try {
            results = sourceRoot.tryToParse();
        } catch (IOException ioException) {
            ioException.printStackTrace();
            System.exit(1);
            return;
        }
        for (ParseResult<CompilationUnit> result : results) {
            if (!result.isSuccessful()) {
                for (Problem problem : result.getProblems()) {
                    hasError = true;
                    System.err.println(problem.toString());
                }
                continue;
            }
            Optional<CompilationUnit> parseResult = result.getResult();
            if (parseResult.isPresent()) {
                CompilationUnit cu = parseResult.get();
                if (cu != null) {
                    cu.accept(new GenericVisitorWithDefaults<Void, Void>() {
                        @Override
                        public Void defaultAction(Node n, Void arg) {
                            recurse(n, 0, "ROOT");
                            return super.defaultAction(n, arg);
                        }
                    }, null);
                }
            }
        }
        if (hasError) {
            System.exit(2);
        }
    }

    public static void recurse(Node n, int level, String parent) {
        String currentStr = n.getClass().toString();
        System.out.println(level + " " + currentStr + " " + parent);
        for (Node nChild : n.getChildNodes()) {
            recurse(nChild, level + 1, currentStr);
        }
    }
}
