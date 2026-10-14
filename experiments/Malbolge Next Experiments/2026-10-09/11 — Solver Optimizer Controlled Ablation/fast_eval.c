/*
 * fast_eval.c — Ultra-fast Malbolge candidate evaluator for synthesis ablation benchmark.
 */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define MEM_SIZE 59049

const char xlat1[] = "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI.v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!BS/|t:Pn6^Ha";
const char xlat2[] = "5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK'X~xDl}REokN:#?G\"i@";

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

int evaluate_string(const char *source, const char *target, int max_steps, char *out_buf, int out_buf_size, int *out_steps) {
  unsigned short mem[MEM_SIZE];
  unsigned short i = 0;
  int len = strlen(source);

  for (int k = 0; k < len; k++) {
    char ch = source[k];
    if (isspace(ch)) continue;
    if (ch < 33 || ch > 126) return 0;
    char instr = xlat1[(ch - 33 + i) % 94];
    if (strchr("ji*p</vo", instr) == NULL) return 0;
    mem[i++] = ch;
  }
  if (i == 0) return 0;

  while (i < MEM_SIZE) {
    mem[i] = op(mem[i - 1], mem[i - 2]);
    i++;
  }

  unsigned short a = 0, c = 0, d = 0;
  int steps = 0;
  int out_pos = 0;

  while (steps < max_steps) {
    steps++;
    unsigned short cell = mem[c];
    unsigned short opcode = (cell + c) % 94;
    int jumped = 0;
    unsigned short c_target = 0;

    switch (opcode) {
      case 4: /* jmp */
        c_target = mem[d];
        jumped = 1;
        break;
      case 5: /* out */
        if (out_pos < out_buf_size - 1) {
          out_buf[out_pos++] = (char)(a % 256);
        }
        break;
      case 23: /* in */
        a = 59048;
        break;
      case 39: /* rot */ {
        unsigned short v = mem[d];
        mem[d] = (v / 3) + (v % 3) * 19683;
        a = mem[d];
        break;
      }
      case 40: /* movd */
        d = mem[d];
        break;
      case 62: /* opr */
        mem[d] = op(a, mem[d]);
        a = mem[d];
        break;
      case 68: /* nop */
        break;
      case 81: /* halt */
        out_buf[out_pos] = '\0';
        *out_steps = steps;
        return (strncmp(out_buf, target, strlen(target)) == 0) ? 1 : 0;
      default:
        break;
    }

    if (jumped) c = c_target;
    if (mem[c] >= 33 && mem[c] <= 126) {
      mem[c] = (unsigned char)xlat2[mem[c] - 33];
    }
    c = (c + 1) % MEM_SIZE;
    d = (d + 1) % MEM_SIZE;
  }

  out_buf[out_pos] = '\0';
  *out_steps = steps;
  return 0;
}

int main(int argc, char **argv) {
  if (argc < 3) {
    fprintf(stderr, "Usage: %s <target> <candidate> [max_steps]\n", argv[0]);
    return 2;
  }
  const char *target = argv[1];
  const char *cand = argv[2];
  int max_steps = (argc >= 4) ? atoi(argv[3]) : 500;

  char out_buf[1024];
  int steps = 0;
  int hit = evaluate_string(cand, target, max_steps, out_buf, sizeof(out_buf), &steps);

  printf("HIT:%d STEPS:%d OUT:%s\n", hit, steps, out_buf);
  return hit ? 0 : 1;
}
