function lowThreshold(values, threshold=0) {
  values = values.map(function(item) {
    if (item > threshold) return item;
    return null;
  });
  return values;
};

module.exports = {
  lowThreshold: lowThreshold
};
