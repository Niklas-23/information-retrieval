import os
from subprocess import check_output
import argparse


def calculated_measure(res_directory, trec_eval_tool, qre_file_path, number_topics, measure):
    result = {}
    for file in os.listdir(res_directory):
        output = check_output([trec_eval_tool, qre_file_path, res_directory+file, "-l2", "-m", measure, "-q"])
        output = output.decode('utf-8')
        per_query_results = output.split("\n")
        total_score = 0.0
        for line in per_query_results:
            if line.strip() == "":
                continue
            result_parts = line.split("\t")
            print("-----------")
            print(result_parts)
            if result_parts[2] == "all":
                continue
            score = float(result_parts[2].strip())
            total_score += score
        submission = file.split(".")[0].split("prime_")[1]
        result[submission] = total_score/number_topics
    return result


def get_result(trec_eval_tool, qre_file_path, prim_result_dir, evaluation_result_file, number_topics):
    file_res = open(evaluation_result_file, "w")
    res_ndcg = calculated_measure(prim_result_dir, trec_eval_tool, qre_file_path, number_topics, "ndcg")
    res_map = calculated_measure(prim_result_dir, trec_eval_tool, qre_file_path, number_topics, "map")
    res_p10 = calculated_measure(prim_result_dir, trec_eval_tool, qre_file_path, number_topics, "P.10")
    file_res.write("System\tnDCG'\tmAP'\tp@10\n")
    for sub in res_ndcg:
        file_res.write(str(sub)+"\t"+str(res_ndcg[sub])+"\t"+str(res_map[sub])+"\t"+str(res_p10[sub])+"\n")
    file_res.close()


def main():
    """
    Sample command :
    python task1_get_results.py -eva "trec_eval" -qre "qrel_task1.tsv" -pri "/All_Trec_Prime/" -res "task1.tsv"
    """
    parser = argparse.ArgumentParser(description='Specify the trec_eval file path, qrel file, '
                                                 'prime results directory and result file  path')

    parser.add_argument('-eva', help='trec_eval tool file path', required=True)
    parser.add_argument('-qre', help='qrel file path', required=True)
    parser.add_argument('-pri', help='prime results directory', required=True)
    parser.add_argument('-res', help='evaluation result file', required=True)
    args = vars(parser.parse_args())
    trec_eval_tool = args['eva']
    qre_file_path = args['qre']
    prim_result_dir = args['pri']
    evaluation_result_file = args['res']
    number_topics = 78.0
    get_result(trec_eval_tool, qre_file_path, prim_result_dir, evaluation_result_file, number_topics)


if __name__ == "__main__":
    main()
