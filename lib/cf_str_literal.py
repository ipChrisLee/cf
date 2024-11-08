anchor_str = "cf"

bist_stdcpp_h_str = """
// 17.4.1.2 Headers

// C
#ifndef _GLIBCXX_NO_ASSERT
#include <cassert>
#endif
#include <cctype>
#include <cerrno>
#include <cfloat>
#include <ciso646>
#include <climits>
#include <clocale>
#include <cmath>
#include <csetjmp>
#include <csignal>
#include <cstdarg>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>

#if __cplusplus >= 201103L
#include <ccomplex>
#include <cfenv>
#include <cinttypes>
#include <cstdbool>
#include <cstdint>
#include <ctgmath>
#include <cwchar>
#include <cwctype>
#include <exception>
#include <stdexcept>
#endif

// C++
#include <algorithm>
#include <bitset>
#include <complex>
#include <deque>
#include <exception>
#include <fstream>
#include <functional>
#include <iomanip>
#include <ios>
#include <iosfwd>
#include <iostream>
#include <istream>
#include <iterator>
#include <limits>
#include <list>
#include <locale>
#include <map>
#include <memory>
#include <new>
#include <numeric>
#include <ostream>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <streambuf>
#include <string>
#include <typeinfo>
#include <utility>
#include <valarray>
#include <vector>

#if __cplusplus >= 201103L
#include <array>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <forward_list>
#include <future>
#include <initializer_list>
#include <mutex>
#include <random>
#include <ratio>
#include <regex>
#include <scoped_allocator>
#include <system_error>
#include <thread>
#include <tuple>
#include <typeindex>
#include <type_traits>
#include <unordered_map>
#include <unordered_set>
#endif
"""

default_cpp_file_str = """\
#include <bits/stdc++.h>

using i32 = int32_t;
using i64 = int64_t;

int main(int argc, char ** argv) {
    std::ios::sync_with_stdio(false); std::cin.tie(nullptr);

    return 0;
}
"""

default_py_file_str = """\
def main():
    pass


if __name__ == '__main__':
    main()
"""

default_clangd_file_str = """\
CompileFlags:
    CompilationDatabase: build/
"""

default_git_ignore_str = """\
build
"""

default_cmakelists_str = """\
cmake_minimum_required(VERSION 3.21)

project("contest")

include_directories("include")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS true)
add_compile_options("-static" "-Wall" "-Wextra" "-Wno-unused-parameter")


file(GLOB cppFiles "*.cpp")
foreach(cppFile ${cppFiles})
    get_filename_component(targetName "${cppFile}" NAME_WE)
    add_executable("${targetName}" "${cppFile}")
endforeach()
"""

default_clangformat_file_str = """\
BasedOnStyle: LLVM
AccessModifierOffset: -2
AlignAfterOpenBracket: Align
AlignConsecutiveAssignments: None
AlignOperands: Align
AllowAllArgumentsOnNextLine: false
AllowAllConstructorInitializersOnNextLine: false
AllowAllParametersOfDeclarationOnNextLine: false
AllowShortBlocksOnASingleLine: Always
AllowShortCaseLabelsOnASingleLine: true
AllowShortFunctionsOnASingleLine: All
AllowShortIfStatementsOnASingleLine: Always
AllowShortLambdasOnASingleLine: All
AllowShortLoopsOnASingleLine: true
AlwaysBreakAfterReturnType: None
AlwaysBreakTemplateDeclarations: MultiLine
BreakBeforeBraces: Custom
BraceWrapping:
  AfterCaseLabel: false
  AfterClass: false
  AfterControlStatement: Never
  AfterEnum: false
  AfterFunction: false
  AfterNamespace: false
  AfterUnion: false
  BeforeCatch: false
  BeforeElse: false
  IndentBraces: false
  SplitEmptyFunction: false
  SplitEmptyRecord: true
BreakBeforeBinaryOperators: None
BreakBeforeTernaryOperators: true
BreakConstructorInitializers: BeforeColon
BreakInheritanceList: BeforeColon
ColumnLimit: 0
CompactNamespaces: true
ContinuationIndentWidth: 4
IndentCaseLabels: true
IndentPPDirectives: BeforeHash
IndentWidth: 4

# About empty lines
KeepEmptyLinesAtTheStartOfBlocks: true
MaxEmptyLinesToKeep: 2
EmptyLineBeforeAccessModifier: Leave
SeparateDefinitionBlocks: Leave

NamespaceIndentation: Inner
ObjCSpaceAfterProperty: false
ObjCSpaceBeforeProtocolList: true
PointerAlignment: Middle
ReflowComments: false
SpaceAfterCStyleCast: true
SpaceAfterLogicalNot: false
SpaceAfterTemplateKeyword: false
SpaceBeforeAssignmentOperators: true
SpaceBeforeCpp11BracedList: false
SpaceBeforeCtorInitializerColon: true
SpaceBeforeInheritanceColon: true
SpaceBeforeParens: ControlStatements
SpaceBeforeRangeBasedForLoopColon: false
SpaceInEmptyParentheses: false
SpacesBeforeTrailingComments: 1
SpacesInAngles: false
SpacesInCStyleCastParentheses: false
SpacesInContainerLiterals: true
SpacesInParentheses: false
SpacesInSquareBrackets: false
TabWidth: 4
UseTab: ForContinuationAndIndentation

SortIncludes: Never

ShortNamespaceLines: 1
"""
