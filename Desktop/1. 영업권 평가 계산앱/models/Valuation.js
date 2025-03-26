const mongoose = require('mongoose');

const valuationSchema = new mongoose.Schema({
  companyName: {
    type: String,
    required: true
  },
  valuationMethod: {
    type: String,
    enum: ['수익가치법', '시장가치법', '원가법'],
    required: true
  },
  // 수익가치법 관련 데이터
  annualProfit: {
    type: Number
  },
  capitalizationRate: {
    type: Number
  },
  // 시장가치법 관련 데이터
  marketMultiplier: {
    type: Number
  },
  comparableCompanies: [{
    name: String,
    multiplier: Number
  }],
  // 원가법 관련 데이터
  replacementCost: {
    type: Number
  },
  depreciation: {
    type: Number
  },
  // 공통 데이터
  evaluationDate: {
    type: Date,
    default: Date.now
  },
  result: {
    type: Number
  },
  notes: {
    type: String
  }
});

module.exports = mongoose.model('Valuation', valuationSchema); 