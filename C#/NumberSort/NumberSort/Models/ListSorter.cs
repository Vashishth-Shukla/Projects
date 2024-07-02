using NumberSort.Models;
using System.Collections.ObjectModel;
using System.Collections.Generic;

public static class ListSorter
{
    public static ObservableCollection<NumberModel> MergSort(ObservableCollection<NumberModel> list)
    {
        if (list == null || list.Count <= 1)
            return list;

        List<NumberModel> sortedList = InternalMergeSort(new List<NumberModel>(list));
        return new ObservableCollection<NumberModel>(sortedList);
    }

    private static List<NumberModel> InternalMergeSort(List<NumberModel> list)
    {
        if (list.Count <= 1)
            return list;

        int middle = list.Count / 2;
        List<NumberModel> left = new List<NumberModel>(list.GetRange(0, middle));
        List<NumberModel> right = new List<NumberModel>(list.GetRange(middle, list.Count - middle));

        left = InternalMergeSort(left);
        right = InternalMergeSort(right);

        return Merge(left, right);
    }

    private static List<NumberModel> Merge(List<NumberModel> left, List<NumberModel> right)
    {
        List<NumberModel> result = new List<NumberModel>();
        int leftIndex = 0, rightIndex = 0;

        while (leftIndex < left.Count && rightIndex < right.Count)
        {
            if (left[leftIndex].Value <= right[rightIndex].Value)
            {
                result.Add(left[leftIndex]);
                leftIndex++;
            }
            else
            {
                result.Add(right[rightIndex]);
                rightIndex++;
            }
        }

        while (leftIndex < left.Count)
        {
            result.Add(left[leftIndex]);
            leftIndex++;
        }

        while (rightIndex < right.Count)
        {
            result.Add(right[rightIndex]);
            rightIndex++;
        }

        return result;
    }
}
