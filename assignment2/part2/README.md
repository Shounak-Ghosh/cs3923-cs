Use the following [instructions](https://github.com/SeattleTestbed/docs/blob/master/EducationalAssignments/DefaultPartTwo.md#how-to-run-your-tests-on-many-reference-monitors) for reference as well.

Copy the `ASGN2_1` folder into RUNNABLE with `wrapper.r2py` and the attack cases inside as well. 

Use the following command inside the `ASGN2_1` folder to test the reference monitors.

```
for referencemonitor in reference_monitor_*; do for testcase in sg7569_*; do python ../repy.py ../restrictions.default ../encasementlib.r2py $referencemonitor $testcase; done; done
```

The output can be saved using the following: 
```
for referencemonitor in reference_monitor_*; do
  for testcase in sg7569_*; do
    python -u ../repy.py ../restrictions.default ../encasementlib.r2py $referencemonitor $testcase 2>&1 | tee -a output.txt
  done
done

```