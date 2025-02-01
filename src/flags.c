#include <stdio.h>
#include <string.h>
#include "flags.h"

void get_flags(flags_t *flags, int argc, char **argv)
{
  if (argc > 1)
  {
    for (int i = 0; i < argc; i++)
    {
      /* Regular flags. */
      if ((strcmp(argv[i], "--verbose") == 0) || strcmp(argv[i], "-V") == 0)
      {
        flags->verbose = 1;
      }

      if ((strcmp(argv[i], "--init") == 0) || strcmp(argv[i], "-i"), 0)
      {
        flags->init = 1;
      }

      if ((strcmp(argv[i], "--ace") == 0) || strcmp(argv[i], "-a"), 0)
      {
        flags->ace = 1;
      }

      if ((strcmp(argv[i], "--help") == 0) || strcmp(argv[i], "-h") == 0)
      {
        flags->help = 1;
      }

      if ((strcmp(argv[i], "--version") == 0) || strcmp(argv[i], "-v") == 0)
      {
        flags->version = 1;
      }

      /* Flags that need values (=). */
      // if (index(argv[i], '=') != NULL)
      // {

      // }
    }
  }

  return;
}
