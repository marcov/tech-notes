# Single-depth loop replacement for nested loops

Used for the following sequence:
```
0     1     2
0     1     3
...
0     1     max
0     2     3
...
0   max-1   max
1     2     3
...
max-2 max-1 max
```

```
/**
 * @brief This helper function is used to replace multiple nested loops, each loop
 * incrementing one index from 0 to 'max', with a single depth loop.
 *
 * @note  The current function is handling the increment of 3 indexes.
 *
 * @param   loop_idxs    pointer to the array containing the indexes.
 * @param   loop_max_idx the maximum index to be reached.
 *
 * @returns true if all loops have been computed.
 */
static inline bool
loop_update_indexes(UINT loop_idxs[3], UINT loop_max_idx)
{
    if (++loop_idxs[2] >= loop_max_idx)
    {
        if (++loop_idxs[1] >= loop_max_idx - 1)
        {
            if (++loop_idxs[0] >= loop_max_idx - 2)
            {
                loop_idxs[0] = 0;
                return true;
            }

            loop_idxs[1] = loop_idxs[0] + 1;
        }

        loop_idxs[2] = loop_idxs[1] + 1;
    }

    return false;
}
```
