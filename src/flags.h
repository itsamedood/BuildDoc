#ifndef FLAGS_H
#define FLAGS_H
#define USAGE "Usage: build [flags] [task]\n"

/**
 * Represents flags passed to the program.
 */
typedef struct Flags
{
  int verbose;
  int init;
  int ace;

  int help;
  int version;
} flags_t;

void get_flags(flags_t *flags, int argc, char **argv);
#endif /* FLAGS_H */
