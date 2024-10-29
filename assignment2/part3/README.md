Use the following [instructions](https://github.com/SeattleTestbed/docs/blob/master/EducationalAssignments/DefaultPartThree.md#how-to-run-your-tests-on-many-reference-monitors) for reference as well.

Copy the `isp_fall_2024_final_attackcases` folder into RUNNABLE with `wrapper.r2py` and the attack cases inside as well. 

Use the following command inside the folder to test the reference monitor against the attack cases.

```
for referencemonitor in reference_monitor_*; do for testcase in *_attackcase*; do python ../repy.py ../restrictions.default ../encasementlib.r2py $referencemonitor $testcase; done; done
```

The output can be saved using the following: 
```
for referencemonitor in reference_monitor_*; do
  for testcase in *_attackcase*; do
    python -u ../repy.py ../restrictions.default ../encasementlib.r2py $referencemonitor $testcase 2>&1 | tee -a output.txt
  done
done

```