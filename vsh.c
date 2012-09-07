/* Version 3 of vsh. Basically a wrapper around 'lxcsu -n -m <slicename>' - Sapan */

#include <unistd.h>
#include <pwd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define VSH_PATH    "/usr/sbin/vsh"
#ifndef PATH_MAX
#define PATH_MAX    4096
#endif

#define LXCSU_PATH  "/usr/sbin/lxcsu"

char* get_current_username (unsigned int uid)
{
    struct passwd *passwd_entry;
    if ((passwd_entry = getpwuid(uid)) == NULL) {
        fprintf(stderr, "Could not look up user record for %d\n", uid);
        return NULL; 
    }

    return (strdup(passwd_entry->pw_name));
}

char **extend_argv(int argc, char **argv, int num_extra_args) {
    int argc2, i;
    char **argv2;

    argc2 = argc + num_extra_args;
    argv2 = (char **) malloc((argc2 + 1) * sizeof(char *));

    if (!argv2)
        return (char **) NULL;

    for (i=0; i<argc; i++) {
        argv2[i+num_extra_args]=strdup(argv[i]); 
    }
    argv2[argc2]=NULL;

    return argv2;
}

#define NUM_LXCSU_EXEC_ARGS 1

int main(int argc, char **argv, char **envp)
{
    char *slice_name;
    char **argv2;
    int argc2;
    char slice_id_str[256];
    unsigned int slice_xid;

    slice_xid = getuid();
    slice_name = get_current_username(slice_xid);
    if (!slice_name) {
        fprintf(stderr,"Could not look up slice name\n");
        goto out_exception;
    }
    
    argv2 = extend_argv(argc, argv, NUM_LXCSU_EXEC_ARGS);
    if (!argv2) goto out_exception;
        
    
    // Populate arguments
    snprintf(slice_id_str, 255, "%u", slice_xid);
    argv2[0] = strdup(LXCSU_PATH);
    argv2[1] = strdup(slice_name);

    if (setuid(geteuid())) goto out_exception;

    execve(LXCSU_PATH, argv2, envp);

out_exception:
    printf("%s\n", strerror(errno));
    return errno;
}
