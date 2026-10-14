#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

static const char xlat1[] = "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha";
static const char xlat2[] = "5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK'X~xDl}REokN:#?G\"i@";

static inline unsigned short op( unsigned short x, unsigned short y )
{
  unsigned short i = 0, j;
  static const unsigned short p9[5] = { 1, 9, 81, 729, 6561 };
  static const unsigned short o[9][9] = {
    { 4, 3, 3, 1, 0, 0, 1, 0, 0 },
    { 4, 3, 5, 1, 0, 2, 1, 0, 2 },
    { 5, 5, 4, 2, 2, 1, 2, 2, 1 },
    { 4, 3, 3, 1, 0, 0, 7, 6, 6 },
    { 4, 3, 5, 1, 0, 2, 7, 6, 8 },
    { 5, 5, 4, 2, 2, 1, 8, 8, 7 },
    { 7, 6, 6, 7, 6, 6, 4, 3, 3 },
    { 7, 6, 8, 7, 6, 8, 4, 3, 5 },
    { 8, 8, 7, 8, 8, 7, 5, 5, 4 },
  };
  for ( j = 0; j < 5; j++ )
    i += o[y / p9[j] % 9][x / p9[j] % 9] * p9[j];
  return ( i );
}

typedef struct {
    int steps;
    int halted;
    int first_output;
    int stop_reason; // 0: FUEL, 1: HALT, 2: INVALID
} RunResult;

RunResult run_candidate(const unsigned char *code, int code_len, int max_steps, int is_current_epoch) {
    unsigned short mem[59049];
    unsigned short i = 0;
    for (int k = 0; k < code_len; k++) {
        if (isspace(code[k])) continue;
        mem[i++] = code[k];
    }
    while (i < 59049) {
        mem[i] = op(mem[i - 1], mem[i - 2]);
        i++;
    }

    unsigned short a = 0, c = 0, d = 0;
    long steps = 0;
    RunResult res = {0, 0, -1, 0};

    while (steps < max_steps) {
        if (mem[c] < 33 || mem[c] > 126) {
            c = (c == 59048) ? 0 : c + 1;
            d = (d == 59048) ? 0 : d + 1;
            continue;
        }
        steps++;
        char instr = xlat1[(mem[c] - 33 + c) % 94];
        if (instr == 'j') d = mem[d];
        else if (instr == 'i') c = mem[d];
        else if (instr == '*') a = mem[d] = mem[d] / 3 + mem[d] % 3 * 19683;
        else if (instr == 'p') a = mem[d] = op(a, mem[d]);
        else if (instr == '<') {
            if (res.first_output < 0) res.first_output = a & 0xFF;
        }
        else if (instr == '/') {
            if (is_current_epoch) a = 59048; // EOF
            else a = 0;
        }
        else if (instr == 'v') {
            res.halted = 1;
            res.stop_reason = 1; // HALT
            break;
        }

        mem[c] = xlat2[mem[c] - 33];
        c = (c == 59048) ? 0 : c + 1;
        d = (d == 59048) ? 0 : d + 1;
    }
    res.steps = steps;
    return res;
}
