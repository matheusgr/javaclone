package com.yourorganization.maven_sample;

import java.util.Optional;

import com.github.javaparser.ParseResult;
import com.github.javaparser.Problem;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.ImportDeclaration;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.visitor.GenericVisitorWithDefaults;

/**
 * Some code that uses JavaParser.
 */
public class LogicPositivizer {

    public static boolean parse(ParseResult<CompilationUnit> result, String unitName) {
        if (!result.isSuccessful()) {
            for (Problem problem : result.getProblems()) {
                System.err.println(problem.toString());
            }
            return false;
        }
        Optional<CompilationUnit> parseResult = result.getResult();
        if (parseResult.isPresent()) {
            CompilationUnit cu = parseResult.get();
            for (ImportDeclaration importDeclaration : cu.getImports()) {
                if (importDeclaration.getName().asString().contains("junit")) {
                    return true;
                }
            }
            String pName = cu.getPrimaryTypeName().orElse(unitName);
            cu.accept(new GenericVisitorWithDefaults<Void, Void>() {
                @Override
                public Void defaultAction(Node n, Void arg) {
                    recurse(pName, n, 0, "ROOT");
                    return super.defaultAction(n, arg);
                }
            }, null);
        }
        return true;
    }

    public static void recurse(String pName, Node n, int level, String parent) {
        String currentStr = n.getClass().getName();
        System.out.println(pName + " " + level + " " + currentStr + " " + parent);
        for (Node nChild : n.getChildNodes()) {
            recurse(pName, nChild, level + 1, currentStr);
        }
    }
}
