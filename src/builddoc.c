#include <stdio.h>
#include "builddoc.h"
#include "flags.h"

/**
 * Entry point.
 */
int main(int argc, char **argv)
{
  flags_t flags = {
    .verbose = 0,
    .init = 0,
    .ace = 0,
    .help = 0,
    .version = 0
  };

  get_flags(&flags, argc, argv);
  printf("Verbose=%d\n", flags.verbose);
}
