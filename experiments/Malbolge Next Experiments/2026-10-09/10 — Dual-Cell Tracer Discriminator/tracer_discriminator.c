/*
 * tracer_discriminator.c — High-performance canonical Malbolge VM with execution tracing
 * and perturbation discrimination for Lutter Quine (59,852 bytes).
 *
 * Part of Malbolge Next Experiments / 2026-10-09 / Compose 10: Dual-Cell Tracer Discriminator.
 */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <malloc.h>
#include <string.h>
#include <openssl/sha.h>

#define MEM_SIZE 59049
#define MAX_CANONICAL_STEPS 75000000ULL

const char xlat2[] = "5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB6v^=I_0/8|jsb9m<.TVac`uY*MK'X~xDl}REokN:#?G\"i@";

static inline unsigned short crazy_op( unsigned short x, unsigned short y )
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

void compute_sha256_hex(const unsigned char *data, size_t len, char *hex_out) {
  unsigned char hash[SHA256_DIGEST_LENGTH];
  SHA256(data, len, hash);
  for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
    sprintf(hex_out + (i * 2), "%02x", hash[i]);
  }
  hex_out[64] = '\0';
}

typedef struct {
  int target_cell;
  int delta;
  unsigned long long steps;
  unsigned long long total_out;
  unsigned long long char_out;
  unsigned long long newline_out;
  unsigned long long d_29454_out_count;
  unsigned long long d_29282_out_count;
  int halted;
  char output_sha256[65];
} TraceResult;

int load_source_into_memory(const char *src_file, unsigned short *mem, size_t *raw_size, size_t *code_size, size_t *newline_size) {
  FILE *f = fopen(src_file, "r");
  if (!f) return -1;
  unsigned short i = 0;
  int x;
  *raw_size = 0;
  *code_size = 0;
  *newline_size = 0;

  while ((x = getc(f)) != EOF) {
    (*raw_size)++;
    if (x == '\n') (*newline_size)++;
    if (isspace(x)) continue;
    (*code_size)++;
    if (i < MEM_SIZE) {
      mem[i++] = x;
    }
  }
  fclose(f);
  while (i < MEM_SIZE) {
    mem[i] = crazy_op(mem[i - 1], mem[i - 2]);
    i++;
  }
  return 0;
}

TraceResult execute_malbolge_vm(unsigned short *mem, int target_cell, int delta, unsigned long long max_steps) {
  TraceResult res;
  memset(&res, 0, sizeof(res));
  res.target_cell = target_cell;
  res.delta = delta;

  if (target_cell >= 0 && target_cell < MEM_SIZE) {
    mem[target_cell] = (mem[target_cell] + delta + MEM_SIZE) % MEM_SIZE;
  }

  unsigned short a = 0, c = 0, d = 0;
  unsigned long long steps = 0;

  /* Buffer for output bytes to compute sha256 */
  size_t out_buf_capacity = 65536;
  unsigned char *out_buf = (unsigned char *)malloc(out_buf_capacity);

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
        if (res.total_out >= out_buf_capacity) {
          out_buf_capacity *= 2;
          out_buf = (unsigned char *)realloc(out_buf, out_buf_capacity);
        }
        out_buf[res.total_out] = (unsigned char)(a % 256);
        res.total_out++;

        if ((a % 256) == 10) res.newline_out++; else res.char_out++;
        if (d == 29454) res.d_29454_out_count++;
        if (d == 29282) res.d_29282_out_count++;
        break;
      case 23: /* in */
        a = 59048; /* EOF */
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
        mem[d] = crazy_op(a, mem[d]);
        a = mem[d];
        break;
      case 68: /* nop */
        break;
      case 81: /* halt */
        res.halted = 1;
        res.steps = steps;
        compute_sha256_hex(out_buf, res.total_out, res.output_sha256);
        free(out_buf);
        return res;
      default:
        break;
    }

    if (jumped) {
      c = c_target;
    }
    if (mem[c] >= 33 && mem[c] <= 126) {
      mem[c] = (unsigned char)xlat2[mem[c] - 33];
    }
    c = (c + 1) % MEM_SIZE;
    d = (d + 1) % MEM_SIZE;
  }

  res.steps = steps;
  compute_sha256_hex(out_buf, res.total_out, res.output_sha256);
  free(out_buf);
  return res;
}

int main(int argc, char **argv) {
  if (argc < 3) {
    fprintf(stderr, "Usage: %s <source.mal> <out.json> [target_cell delta]\n", argv[0]);
    return 1;
  }
  const char *src_file = argv[1];
  const char *json_out_file = argv[2];
  int target_cell = -1;
  int delta = 0;

  if (argc >= 5) {
    target_cell = atoi(argv[3]);
    delta = atoi(argv[4]);
  }

  unsigned short *mem = (unsigned short *)malloc(sizeof(unsigned short) * MEM_SIZE);
  size_t raw_size = 0, code_size = 0, newline_size = 0;

  if (load_source_into_memory(src_file, mem, &raw_size, &code_size, &newline_size) != 0) {
    fprintf(stderr, "Failed to load source file: %s\n", src_file);
    free(mem);
    return 1;
  }

  TraceResult res = execute_malbolge_vm(mem, target_cell, delta, MAX_CANONICAL_STEPS);
  free(mem);

  FILE *jf = fopen(json_out_file, "w");
  if (!jf) {
    fprintf(stderr, "Failed to open json output file: %s\n", json_out_file);
    return 1;
  }

  fprintf(jf, "{\n");
  fprintf(jf, "  \"source_file\": \"%s\",\n", src_file);
  fprintf(jf, "  \"raw_bytes\": %zu,\n", raw_size);
  fprintf(jf, "  \"code_bytes\": %zu,\n", code_size);
  fprintf(jf, "  \"newline_bytes\": %zu,\n", newline_size);
  fprintf(jf, "  \"target_cell\": %d,\n", res.target_cell);
  fprintf(jf, "  \"delta\": %d,\n", res.delta);
  fprintf(jf, "  \"steps\": %llu,\n", res.steps);
  fprintf(jf, "  \"halted\": %s,\n", res.halted ? "true" : "false");
  fprintf(jf, "  \"total_out\": %llu,\n", res.total_out);
  fprintf(jf, "  \"char_out\": %llu,\n", res.char_out);
  fprintf(jf, "  \"newline_out\": %llu,\n", res.newline_out);
  fprintf(jf, "  \"d_29454_out_count\": %llu,\n", res.d_29454_out_count);
  fprintf(jf, "  \"d_29282_out_count\": %llu,\n", res.d_29282_out_count);
  fprintf(jf, "  \"output_sha256\": \"%s\"\n", res.output_sha256);
  fprintf(jf, "}\n");
  fclose(jf);

  return 0;
}
