from cffi import FFI

ffi = FFI()

ffi.set_source("_cdb2api",
    """
        #include <cdb2api.h>
    """,
    libraries=["cdb2api", "protobuf-c"])
ffi.cdef("""
    enum cdb2_hndl_alloc_flags {
        CDB2_READ_INTRANS_RESULTS = 2,
        CDB2_DIRECT_CPU           = 4,
        CDB2_RANDOM               = 8,
        CDB2_RANDOMROOM           = 16
    };

    enum cdb2_request_type {
        CDB2_REQUEST_CDB2QUERY = 1,
        CDB2_REQUEST_SQLQUERY = 2,
        CDB2_REQUEST_DBINFO = 3
    };

    enum cdb2_errors {
        CDB2_OK                    =  0,
        CDB2_OK_DONE               =  1,
        CDB2ERR_CONNECT_ERROR      = -1,
        CDB2ERR_NOTCONNECTED       = -2,
        CDB2ERR_PREPARE_ERROR      = -3,
        CDB2ERR_IO_ERROR           = -4,
        CDB2ERR_INTERNAL           = -5,
        CDB2ERR_NOSTATEMENT        = -6,
        CDB2ERR_BADCOLUMN          = -7,
        CDB2ERR_BADSTATE           = -8,
        CDB2ERR_ASYNCERR           = -9,
        CDB2_OK_ASYNC              = -10,

        CDB2ERR_INVALID_ID              = -12,
        CDB2ERR_RECORD_OUT_OF_RANGE     = -13,

        CDB2ERR_REJECTED                = -15,
        CDB2ERR_STOPPED                 = -16,
        CDB2ERR_BADREQ                  = -17,
        CDB2ERR_DBCREATE_FAILED         = -18,

        CDB2ERR_THREADPOOL_INTERNAL     = -20,  /* some error in threadpool code */
        CDB2ERR_READONLY                = -21,

        CDB2ERR_NOMASTER                = -101,
        CDB2ERR_UNTAGGED_DATABASE       = -102,
        CDB2ERR_CONSTRAINTS             = -103,
        CDB2ERR_DEADLOCK                =  203,

        CDB2ERR_TRAN_IO_ERROR           = -105,
        CDB2ERR_ACCESS                  = -106,

        CDB2ERR_TRAN_MODE_UNSUPPORTED   = -107,

        CDB2ERR_VERIFY_ERROR            = 2,
        CDB2ERR_FKEY_VIOLATION          = 3,
        CDB2ERR_NULL_CONSTRAINT         = 4,

        CDB2ERR_CONV_FAIL               = 113,
        CDB2ERR_NONKLESS                = 114,
        CDB2ERR_MALLOC                  = 115,
        CDB2ERR_NOTSUPPORTED            = 116,

        CDB2ERR_DUPLICATE               =  299,
        CDB2ERR_TZNAME_FAIL             =  401,

        CDB2ERR_UNKNOWN                 =  300

    };

    enum cdb2_api_const
    {
        CDB2_MAX_KEYS=28,
        CDB2_MAX_SERVER_KEY_SIZE=512,
        CDB2_MAX_CLIENT_KEY_SIZE=256,
        CDB2_MAX_ASK_ARRAY=1024,
        CDB2_MAX_ASK_SEGS=511, // (CDB2_MAX_ASK_ARRAY-2)/2,
        CDB2_MAX_BLOB_FIELDS=15,
        CDB2_MAX_TZNAME=36
    } ;

    /* New comdb2tm definition. */
    typedef struct cdb2_tm
    {
        int tm_sec;
        int tm_min;
        int tm_hour;
        int tm_mday;
        int tm_mon;
        int tm_year;
        int tm_wday;
        int tm_yday;
        int tm_isdst;
    }
    cdb2_tm_t;

    struct cdb2_effects_type {
        int num_affected;
        int num_selected;
        int num_updated;
        int num_deleted;
        int num_inserted;
    };

    /* datetime type definition */
    typedef struct cdb2_client_datetime {
        cdb2_tm_t           tm;
        unsigned int        msec;
        char                tzname[...];
    } cdb2_client_datetime_t;

    /* microsecond-precision datetime type definition */
    typedef struct cdb2_client_datetimeus {
        cdb2_tm_t           tm;
        unsigned int        usec;
        char                tzname[...];
    } cdb2_client_datetimeus_t;

    /* interval types definition */
    typedef struct cdb2_client_intv_ym {
        int                 sign;       /* sign of the interval, +/-1 */
        unsigned int        years;      /* interval year */
        unsigned int        months;     /* interval months [0-11] */
    } cdb2_client_intv_ym_t;

    typedef struct cdb2_client_intv_ds {
        int                 sign;       /* sign of the interval, +/-1 */
        unsigned int        days;       /* interval days    */
        unsigned int        hours;      /* interval hours   */
        unsigned int        mins;       /* interval minutes */
        unsigned int        sec;        /* interval sec     */
        unsigned int        msec;       /* msec             */
    } cdb2_client_intv_ds_t;

    typedef struct cdb2_client_intv_dsus {
        int                 sign;       /* sign of the interval, +/-1 */
        unsigned int        days;       /* interval days    */
        unsigned int        hours;      /* interval hours   */
        unsigned int        mins;       /* interval minutes */
        unsigned int        sec;        /* interval sec     */
        unsigned int        usec;       /* usec             */
    } cdb2_client_intv_dsus_t;

    typedef enum cdb2_coltype {
        CDB2_INTEGER   = 1,
        CDB2_REAL      = 2,
        CDB2_CSTRING   = 3,
        CDB2_BLOB      = 4,
        CDB2_DATETIME  = 6,
        CDB2_INTERVALYM= 7,
        CDB2_INTERVALDS= 8,
        CDB2_DATETIMEUS= 9,
        CDB2_INTERVALDSUS=10
    } cdb2_coltype;

    typedef struct cdb2_hndl cdb2_hndl_tp;
    typedef struct cdb2_effects_type cdb2_effects_tp;
    typedef struct cdb2_effects_type effects_tp;

    void cdb2_set_comdb2db_config(char *cfg_file);
    void cdb2_set_comdb2db_info(char *cfg_info);

    int cdb2_open(cdb2_hndl_tp **hndl, const char *dbname, const char *type, int flags);
    int cdb2_clone(cdb2_hndl_tp **hndl, cdb2_hndl_tp *c_hndl);

    int cdb2_next_record(cdb2_hndl_tp *hndl);

    int cdb2_get_effects(cdb2_hndl_tp *hndl, cdb2_effects_tp *effects);

    int cdb2_close(cdb2_hndl_tp* hndl);

    int cdb2_run_statement(cdb2_hndl_tp *hndl, const char *sql);
    int cdb2_run_statement_typed(cdb2_hndl_tp *hndl, const char *sql, int ntypes, int *types);

    int cdb2_numcolumns(cdb2_hndl_tp* hndl);
    const char* cdb2_column_name(cdb2_hndl_tp* hndl, int col);
    int cdb2_column_type(cdb2_hndl_tp* hndl, int col);
    int cdb2_column_size(cdb2_hndl_tp* hndl, int col);
    void* cdb2_column_value(cdb2_hndl_tp* hndl, int col);
    const char* cdb2_errstr(cdb2_hndl_tp* hndl);

    void cdb2_use_hint(cdb2_hndl_tp* hndl);

    int cdb2_bind_param(cdb2_hndl_tp *hndl, const char *name, int type, const void *varaddr, int length);
    int cdb2_bind_index(cdb2_hndl_tp *hndl, int index, int type, const void *varaddr, int length);
    int cdb2_clearbindings(cdb2_hndl_tp *hndl);

    /* SOCKPOOL CLIENT APIS */
    int cdb2_socket_pool_get(const char *typestr, int dbnum, int *port); /* returns the fd.*/
    void cdb2_socket_pool_donate_ext(const char* typestr, int fd, int ttl, int dbnum, int flags, void *destructor, void *voidargs);

    const char* cdb2_dbname(cdb2_hndl_tp* hndl);
""")

if __name__ == '__main__':
    ffi.compile()
